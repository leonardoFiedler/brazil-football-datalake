import boto3
from io import BytesIO
from bs4 import BeautifulSoup
import requests
import datetime
import unidecode
import polars as pl
from dataclasses import dataclass

@dataclass
class ClubsValidation():
    ctn_dt_foundation: int = 0
    ctn_cnpj: int = 0
    ctn_stadium: int = 0
    ctn_colors: int = 0
    ctn_president: int = 0
    ctn_address: int = 0
    ctn_cep: int = 0

def display_teams_data(teams: list):
    for team in teams:
        name = team['team_name']
        found = team['foundation_date'] if 'foundation_date' in team.keys() else None
        cnpj = team['cnpj'] if 'cnpj' in team.keys() else None
        stadium = team['stadium'] if 'stadium' in team.keys() else None
        colors = team['colors'] if 'colors' in team.keys() else None
        president = team['president_name'] if 'president_name' in team.keys() else None
        address = team['address'] if 'address' in team.keys() else None
        cep = team['cep'] if 'cep' in team.keys() else None
        
        print(f"name: {name}   | date: {found}  | cnpj: {cnpj}  | stadium: {stadium}    | colors: {colors}  | president_name: {president}    | address: {address}   | cep: {cep}")

def write_parquet(client, df, bucket, key):
    parquet_io = BytesIO()
    df.write_parquet(parquet_io)
    parquet_io.seek(0)
    return client.upload_fileobj(parquet_io, bucket, key)

def execute(content, cv: ClubsValidation):
    teams = []
    team_data = {}
    team_name = ""

    for item in content.findChildren():
        tag = item.name
        
        if tag == 'h3':
            # Last tg "h3" is "Compartilhe isso"
            if len(team_data.keys()) > 0:
                teams.append(team_data)
            
            team_name = unidecode.unidecode(item.text.strip().lower())
            
            team_data = {'team_name': team_name}
        elif tag == 'p':
            txt = unidecode.unidecode(item.text.strip().lower())
            prefix = txt.split(" ")[0].replace(":", "").replace("-", "")
            
            if "data" == prefix:
                dt_found = txt.split(" ")[3]
                
                if len(dt_found) != 10:
                    print(f"Found diferent value '{dt_found}', ignoring '{txt}' for club '{team_name}'.")
                    continue
                
                if "." in dt_found:
                    dt_pattern = "%d.%m.%Y"
                else:
                    dt_pattern = "%d/%m/%Y"
                    
                dt_found = datetime.datetime.strptime(dt_found, dt_pattern).strftime("%Y-%m-%d")
                team_data["foundation_date"] = dt_found
                cv.ctn_dt_foundation += 1
            
            if "cgc/mf" == prefix:
                txt_cnpj = txt.replace(u'\xa0', u' ').split(" ")[2]
                team_data["cnpj"] = txt_cnpj.strip()
                cv.ctn_cnpj += 1
            
            if "estadio" == prefix:
                txt_stadium = txt.replace("estadio:", "")
                team_data["stadium"] = None if len(txt_stadium) == 0 else txt_stadium.strip()
                
                if team_data["stadium"] is not None:
                    cv.ctn_stadium += 1

            if "cores" == prefix:
                txt_colors = txt.replace("cores oficiais", "").replace(":", "").replace("-", "")
                team_data["colors"] = None if len(txt_colors) == 0 else txt_colors.strip()
                
                if team_data["colors"] is not None:
                    cv.ctn_colors += 1
            
            if "presidente" == prefix:
                txt_president = txt.replace("presidente", "").replace("/diretor executivo", "").replace(":", "")
                team_data["president_name"] = None if len(txt_president) == 0 else txt_president.strip()
                
                if team_data["president_name"] is not None:
                    cv.ctn_president += 1
            
            if "diretor" == prefix:
                txt_president = txt.replace("diretor presidente", "").replace(":", "")
                team_data["president_name"] = None if len(txt_president) == 0 else txt_president.strip()
                
                if team_data["president_name"] is not None:
                    cv.ctn_president += 1
            
            if "endereco" == prefix:
                txt_address = txt.replace("endereco", "").replace(":", "")
                team_data["address"] = None if len(txt_address) == 0 else txt_address.strip()
                
                if team_data["address"] is not None:
                    cv.ctn_address += 1

            if "cep" == prefix:
                txt_cep = txt.replace("cep", "").replace(":", "")
                team_data["cep"] = None if len(txt_cep) == 0 else txt_cep.strip()
                
                if team_data["cep"] is not None:
                    cv.ctn_cep += 1
    
    return teams

def validate(teams: list, cv: ClubsValidation, content):
    # Assert quantity of clubs downloaded is correct
    assert len(content.findChildren("h3")) - 1 == len(teams)
    assert 30 == cv.ctn_dt_foundation
    assert 18 == cv.ctn_cnpj
    assert 28 == cv.ctn_stadium
    assert 31 == cv.ctn_colors
    assert 31 == cv.ctn_president
    assert 31 == cv.ctn_address
    assert 29 == cv.ctn_cep    

def process():
    cv: ClubsValidation = ClubsValidation()
    
    print("Creating conn with S3")
    client = boto3.client(
        "s3",
        aws_access_key_id = "minio",
        aws_secret_access_key = "minio123",
        endpoint_url = "http://minio:9000",
        region_name='us-east-1'
    )
    
    print("Requesting")
    r = requests.get("https://fcf.com.br/clubes-filiados/")

    soup = BeautifulSoup(r.text, "html.parser")

    content = soup.find(class_="entry-content")
    
    print("Executing")
    teams = execute(content, cv)
    
    print("Validating")
    validate(teams, cv, content)
    
    print("Writing")
    df = pl.from_dicts(teams)
    write_parquet(client, df, "datalake", "landing/2024/sc_teams.parquet")
    
    print("All done!!!")

if __name__ == '__main__':
    process()