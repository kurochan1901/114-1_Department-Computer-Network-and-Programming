import sqlite3, os, sys
from pathlib import Path

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "ID_data.db"

SQL_TEXT = r"""
-- select and delete incorret ID
BEGIN;
WITH incorrect AS (
    SELECT *
    FROM ID_table
    WHERE ID IS NULL
       OR length(ID) <> 9
       OR ID NOT GLOB '[A-Z][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]'
)

    DELETE FROM ID_table
    WHERE ID IN (SELECT ID FROM incorrect);
COMMIT;

-- create new table
CREATE TABLE IF NOT EXISTS region_code (
  code TEXT PRIMARY KEY
       CHECK (length(code)=1 AND code BETWEEN 'A' AND 'Z'),
  city_name TEXT NOT NULL
);

-- inport county and code data
INSERT INTO region_code (code, city_name) VALUES
('A','台北市'),('B','台中市'),('C','基隆市'),('D','台南市'),('E','高雄市'),
('F','台北縣'),('G','宜蘭縣'),('H','桃園縣'),('I','嘉義市'),('J','新竹縣'),
('K','苗栗縣'),('L','台中縣'),('M','南投縣'),('N','彰化縣'),('O','新竹市'),
('P','雲林縣'),('Q','嘉義縣'),('R','台南縣'),('S','高雄縣'),('T','屏東縣'),
('U','花蓮縣'),('V','台東縣'),('W','金門縣'),('X','澎湖縣'),('Y','陽明山'),
('Z','連江縣');

-- update county data to ID_table
-- preview
SELECT i.ID,
       substr(i.ID,1,1) AS code,
       rc.city_name
FROM ID_table i
LEFT JOIN region_code rc
  ON rc.code = substr(trim(i.ID),1,1);

-- update cityname
BEGIN;

UPDATE ID_table AS i
SET country = (
  SELECT rc.city_name
  FROM region_code rc
  WHERE rc.code = substr(i.ID,1,1)
);

COMMIT;

-- update gender data to ID_table
BEGIN;

UPDATE ID_table
SET gender = CASE substr(ID, 2, 1)
               WHEN '1' THEN '男性'
               WHEN '2' THEN '女性'
               WHEN '8' THEN '男性(居留)'
               WHEN '9' THEN '女性(居留)'
               ELSE gender     -- 第二碼不是 1/2/8/9 就不動
             COMMIT;
WHERE substr(trim(ID), 2, 1) IN ('1','2','8','9');

COMMIT;

-- create new table of citizenship
CREATE TABLE IF NOT EXISTS citizenship_code (
  code TEXT PRIMARY KEY
       CHECK (length(code)=1 AND code BETWEEN '0' AND '9'),
  citizenship TEXT NOT NULL
);
-- insert data
INSERT OR REPLACE INTO citizenship_code (code, citizenship) VALUES
('0','在台灣出生之本國籍民'),
('1','在台灣出生之本國籍民'),
('2','在台灣出生之本國籍民'),
('3','在台灣出生之本國籍民'),
('4','在台灣出生之本國籍民'),
('5','在台灣出生之本國籍民'),
('6','入籍國民，原為外國人'),
('7','入籍國民，原為無戶籍國民'),
('8','入籍國民，原為香港居民或澳門居民'),
('9','入籍國民，原為大陸地區居民');

-- preview
SELECT i.ID,
       substr(i.ID,3,1) AS code1,
       cc.citizenship
FROM ID_table i
LEFT JOIN citizenship_code AS cc
  ON cc.code = substr(trim(i.ID),3,1);
  
-- add citizenship data to ID_table
BEGIN;

UPDATE ID_table AS i
SET citizenship = (
  SELECT cc.citizenship
  FROM citizenship_code AS cc
  WHERE cc.code = substr(ID, 3, 1)
)
WHERE EXISTS (
  SELECT 1
  FROM citizenship_code AS cc
  WHERE cc.code = substr(ID, 3, 1)
);

COMMIT;

-- add new column for city number in TABLE region_code
--ALTER TABLE region_code ADD COLUMN city_num INTEGER;

-- update region_code
UPDATE region_code
SET city_num = CASE code
  WHEN 'A' THEN 10 WHEN 'B' THEN 11 WHEN 'C' THEN 12 WHEN 'D' THEN 13 WHEN 'E' THEN 14
  WHEN 'F' THEN 15 WHEN 'G' THEN 16 WHEN 'H' THEN 17 WHEN 'I' THEN 34 WHEN 'J' THEN 18
  WHEN 'K' THEN 19 WHEN 'L' THEN 20 WHEN 'M' THEN 21 WHEN 'N' THEN 22 WHEN 'O' THEN 35
  WHEN 'P' THEN 23 WHEN 'Q' THEN 24 WHEN 'R' THEN 25 WHEN 'S' THEN 26 WHEN 'T' THEN 27
  WHEN 'U' THEN 28 WHEN 'V' THEN 29 WHEN 'W' THEN 32 WHEN 'X' THEN 30 WHEN 'Y' THEN 31
  WHEN 'Z' THEN 33
COMMIT;

-- add verify code to ID
-- preview
WITH sums AS (
  SELECT
    i.ID AS id9,
    CAST(rc.city_num/10 AS INT)*1 + (rc.city_num % 10)*9
    + CAST(substr(trim(i.ID),2,1) AS INT)*8
    + CAST(substr(trim(i.ID),3,1) AS INT)*7
    + CAST(substr(trim(i.ID),4,1) AS INT)*6
    + CAST(substr(trim(i.ID),5,1) AS INT)*5
    + CAST(substr(trim(i.ID),6,1) AS INT)*4
    + CAST(substr(trim(i.ID),7,1) AS INT)*3
    + CAST(substr(trim(i.ID),8,1) AS INT)*2
    + CAST(substr(trim(i.ID),9,1) AS INT)*1 AS s_no_last
  FROM ID_table i
  JOIN region_code rc
    ON rc.code = substr(trim(i.ID), 1, 1)
  WHERE length(trim(i.ID)) = 9
    AND trim(i.ID) GLOB '[A-Z][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]'
)
SELECT
  id9 AS id_9,
  (10 - (s_no_last % 10)) % 10 AS check_digit,
  id9 || ((10 - (s_no_last % 10)) % 10) AS id_10
FROM sums
LIMIT 50;

-- update 10th code to ID_table
WITH calc AS (
  SELECT
    i.rowid AS rid,
    i.ID    AS id9,
    CAST(rc.city_num/10 AS INT)*1 + (rc.city_num % 10)*9
    + CAST(substr(trim(i.ID),2,1) AS INT)*8
    + CAST(substr(trim(i.ID),3,1) AS INT)*7
    + CAST(substr(trim(i.ID),4,1) AS INT)*6
    + CAST(substr(trim(i.ID),5,1) AS INT)*5
    + CAST(substr(trim(i.ID),6,1) AS INT)*4
    + CAST(substr(trim(i.ID),7,1) AS INT)*3
    + CAST(substr(trim(i.ID),8,1) AS INT)*2
    + CAST(substr(trim(i.ID),9,1) AS INT)*1 AS s_no_last
  FROM ID_table i
  JOIN region_code rc
    ON rc.code = substr(trim(i.ID),1,1)
  WHERE length(trim(i.ID)) = 9
    AND trim(i.ID) GLOB '[A-Z][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]'
)
UPDATE ID_table
SET ID = (SELECT id9 || ((10 - (s_no_last % 10)) % 10) FROM calc WHERE calc.rid = ID_table.rowid)
WHERE rowid IN (SELECT rid FROM calc);

-- new view for recognize if the ID is right
DROP VIEW IF EXISTS validate_one_id;
CREATE VIEW validate_one_id AS
WITH input AS (SELECT idForTest AS id FROM id_input),
parts AS (
  SELECT
    id,
    substr(id,1,1)  AS c1,
    substr(id,2,1)  AS d2,
    substr(id,3,1)  AS d3,
    substr(id,4,1)  AS d4,
    substr(id,5,1)  AS d5,
    substr(id,6,1)  AS d6,
    substr(id,7,1)  AS d7,
    substr(id,8,1)  AS d8,
    substr(id,9,1)  AS d9,
    substr(id,10,1) AS d10
  FROM input
),
joined AS (
  SELECT p.*, rc.city_name, rc.city_num, cc.citizenship
  FROM parts p
  LEFT JOIN region_code      rc ON rc.code = p.c1
  LEFT JOIN citizenship_code cc ON cc.code = p.d3
),
flags AS (
  SELECT j.*,
    (length(j.id)=10
     AND j.id GLOB '[A-Z][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]'
     AND j.d2 IN ('1','2','8','9')
     AND j.city_num IS NOT NULL) AS valid_basic,
    (
      CAST(j.city_num/10 AS INT)*1 + (j.city_num%10)*9
      + CAST(j.d2 AS INT)*8 + CAST(j.d3 AS INT)*7 + CAST(j.d4 AS INT)*6
      + CAST(j.d5 AS INT)*5 + CAST(j.d6 AS INT)*4 + CAST(j.d7 AS INT)*3
      + CAST(j.d8 AS INT)*2 + CAST(j.d9 AS INT)*1 + CAST(j.d10 AS INT)*1
    ) % 10 = 0 AS valid_checksum
  FROM joined j
)
SELECT
  id,
  CASE WHEN valid_basic AND valid_checksum THEN '真' ELSE '假' END AS 是否為真,
  CASE WHEN NOT (valid_basic AND valid_checksum) THEN '請重新輸入'
       ELSE CASE d2 WHEN '1' THEN '男性'
                    WHEN '2' THEN '女性'
                    WHEN '8' THEN '男性(居留)'
                    WHEN '9' THEN '女性(居留)' END
  END AS 性別,
  CASE WHEN valid_basic AND valid_checksum THEN city_name END AS 縣市,
  CASE WHEN valid_basic AND valid_checksum THEN citizenship END AS 第三碼意義,
  CASE WHEN valid_basic AND valid_checksum
       THEN printf('%s %s %s', city_name,
                   CASE d2 WHEN '1' THEN '男性'
                           WHEN '2' THEN '女性'
                           WHEN '8' THEN '男性(居留)'
                           WHEN '9' THEN '女性(居留)' END,
                   COALESCE(citizenship,''))
       ELSE '請重新輸入'
  END AS 說明
FROM flags;

"""

def main():
    if not os.path.exists(DB_PATH):
        print(f"[!] 找不到 {DB_PATH}，請把本檔與資料庫放在同一資料夾。")
        sys.exit(1)

    con = sqlite3.connect(DB_PATH)
    try:
        con.execute("PRAGMA foreign_keys = ON;")
        # 一次跑多條 SQL（含 CREATE / INSERT / UPDATE / VIEW ）
        con.commit()
        print("SQL 腳本已成功套用到資料庫。")
    except Exception as e:
        con.rollback()
        print("執行失敗：", e)
        sys.exit(2)
    finally:
        con.close()

if __name__ == "__main__":
    main()
