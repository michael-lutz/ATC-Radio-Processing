import boto3
import gzip
import json
import pandas as pd

def main():
    s3 = boto3.resource("s3")

    df_combined = pd.DataFrame()

    for hour in range(24):
        hour = f"{hour:02}"
        df_hour = pd.DataFrame()
        for minute in range(60):
            minute = f"{minute:02}"
            for second in range(12): # Data increments by 5 seconds
                second = f"{second*5:02}"
                time_str = "readsb-hist/2022/01/08/" + hour + minute + second + "Z.json.gz"
                df_combined = df_combined.append(get_df(s3, time_str))
                df_hour = df_hour.append(get_df(s3, time_str))
        df_hour.to_csv(hour, index=False)
        
    
    df_combined.to_csv('01-08-2022', index=False)

def get_df(s3_instance, time_str):
    obj = s3_instance.Object("atc-speech-recognition", time_str)
    with gzip.GzipFile(fileobj=obj.get()["Body"]) as gzipfile:
        content = gzipfile.read()
        json_file = json.loads(content)['aircraft']

        df = pd.DataFrame.from_dict(json_file)
        df['time'] = json.loads(content)['now']
        return df[(df['lat']-32.8998)**2+(df['lon']+97.0403)**2<6.25]

if __name__ == "__main__":
    main()