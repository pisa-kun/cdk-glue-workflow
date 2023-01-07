@echo off

@REM 今日の日付を/を省いて取得
set today=%date:~0,4%%date:~5,2%%date:~8,2%

@REM 取得した日付をもとにファイル置き場を作成
mkdir %today%

@REM データダウンロード
aws s3 cp s3://upload-pisakun-bucket/Test/ %today% --recursive