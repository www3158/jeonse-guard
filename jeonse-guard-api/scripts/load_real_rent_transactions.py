import csv
import sys
from datetime import date
from pathlib import Path

from psycopg.rows import dict_row

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.database import get_connection


APT = "\uc544\ud30c\ud2b8"
VILLA = "\uc5f0\ub9bd\ub2e4\uc138\ub300"
OFFICETEL = "\uc624\ud53c\uc2a4\ud154"
SINGLE_MULTI = "\ub2e8\ub3c5\ub2e4\uac00\uad6c"
JEONSE = "\uc804\uc138"

COL_REGION = "\uc2dc\uad70\uad6c"
COL_JIBUN = "\ubc88\uc9c0"
COL_BONBUN = "\ubcf8\ubc88"
COL_BUBUN = "\ubd80\ubc88"
COL_COMPLEX = "\ub2e8\uc9c0\uba85"
COL_BUILDING = "\uac74\ubb3c\uba85"
COL_LEASE_TYPE = "\uc804\uc6d4\uc138\uad6c\ubd84"
COL_AREA = "\uc804\uc6a9\uba74\uc801(\u33a1)"
COL_CONTRACT_AREA = "\uacc4\uc57d\uba74\uc801(\u33a1)"
COL_YM = "\uacc4\uc57d\ub144\uc6d4"
COL_DAY = "\uacc4\uc57d\uc77c"
COL_DEPOSIT = "\ubcf4\uc99d\uae08(\ub9cc\uc6d0)"
COL_RENT = "\uc6d4\uc138\uae08(\ub9cc\uc6d0)"
COL_FLOOR = "\uce35"
COL_BUILT_YEAR = "\uac74\ucd95\ub144\ub3c4"
COL_ROAD = "\ub3c4\ub85c\uba85"
COL_PERIOD = "\uacc4\uc57d\uae30\uac04"
COL_CONTRACT_TYPE = "\uacc4\uc57d\uad6c\ubd84"
COL_RENEWAL = "\uac31\uc2e0\uc694\uad6c\uad8c \uc0ac\uc6a9"
COL_PREV_DEPOSIT = "\uc885\uc804\uacc4\uc57d \ubcf4\uc99d\uae08(\ub9cc\uc6d0)"
COL_PREV_RENT = "\uc885\uc804\uacc4\uc57d \uc6d4\uc138(\ub9cc\uc6d0)"
COL_HOUSING_TYPE = "\uc8fc\ud0dd\uc720\ud615"
COL_ROAD_CONDITION = "\ub3c4\ub85c\uc870\uac74"


DDL = """
CREATE TABLE IF NOT EXISTS stg_real_rent_transactions (
    id BIGSERIAL PRIMARY KEY,
    source_file TEXT NOT NULL,
    source_row_no INTEGER NOT NULL,
    property_type VARCHAR(20) NOT NULL,
    property_type_kr VARCHAR(50) NOT NULL,
    address_region TEXT,
    sido TEXT,
    sigungu TEXT,
    eupmyeondong TEXT,
    jibun TEXT,
    bonbun TEXT,
    bubun TEXT,
    complex_name TEXT,
    lease_type VARCHAR(20),
    area_m2 NUMERIC(12, 4),
    contract_year_month VARCHAR(6),
    contract_day VARCHAR(2),
    contract_date DATE,
    deposit_won BIGINT,
    monthly_rent_won BIGINT,
    floor INTEGER,
    built_year INTEGER,
    road_name TEXT,
    contract_period TEXT,
    contract_type TEXT,
    renewal_right_used TEXT,
    previous_deposit_won BIGINT,
    previous_monthly_rent_won BIGINT,
    housing_type TEXT,
    road_condition TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE (source_file, source_row_no)
);

CREATE INDEX IF NOT EXISTS idx_stg_real_rent_type_date
    ON stg_real_rent_transactions (property_type, contract_date);
CREATE INDEX IF NOT EXISTS idx_stg_real_rent_region
    ON stg_real_rent_transactions (address_region);
CREATE INDEX IF NOT EXISTS idx_stg_real_rent_deposit
    ON stg_real_rent_transactions (deposit_won);
"""


COPY_SQL = """
COPY stg_real_rent_transactions (
    source_file, source_row_no, property_type, property_type_kr,
    address_region, sido, sigungu, eupmyeondong, jibun, bonbun, bubun,
    complex_name, lease_type, area_m2, contract_year_month, contract_day,
    contract_date, deposit_won, monthly_rent_won, floor, built_year, road_name,
    contract_period, contract_type, renewal_right_used, previous_deposit_won,
    previous_monthly_rent_won, housing_type, road_condition
) FROM STDIN
"""


TYPE_BY_NAME = {
    APT: ("APT", APT),
    VILLA: ("VILLA", VILLA),
    OFFICETEL: ("OFFICETEL", OFFICETEL),
    SINGLE_MULTI: ("SINGLE_MULTI", SINGLE_MULTI),
}


def clean(value):
    if value is None:
        return None
    value = str(value).strip()
    return value if value and value != "-" else None


def int_value(value, multiplier=1):
    value = clean(value)
    if value is None:
        return None
    try:
        return int(value.replace(",", "")) * multiplier
    except ValueError:
        return None


def decimal_value(value):
    value = clean(value)
    if value is None:
        return None
    try:
        return value.replace(",", "")
    except ValueError:
        return None


def contract_date(year_month, day):
    year_month = clean(year_month)
    day = clean(day)
    if not year_month or not day or len(year_month) != 6:
        return None
    try:
        return date(int(year_month[:4]), int(year_month[4:6]), int(day))
    except ValueError:
        return None


def split_region(region):
    parts = (clean(region) or "").split()
    return (
        parts[0] if len(parts) > 0 else None,
        parts[1] if len(parts) > 1 else None,
        parts[2] if len(parts) > 2 else None,
    )


def detect_type(path):
    for key, value in TYPE_BY_NAME.items():
        if key in path.name:
            return value
    return None


def detect_encoding(path):
    for encoding in ("utf-8-sig", "cp949", "euc-kr"):
        try:
            with path.open("r", encoding=encoding) as f:
                f.read(4096)
            return encoding
        except UnicodeDecodeError:
            continue
    raise UnicodeDecodeError("csv", b"", 0, 1, "unsupported csv encoding")


def iter_rows(path, property_type, property_type_kr):
    with path.open("r", encoding=detect_encoding(path), newline="") as f:
        while True:
            pos = f.tell()
            line = f.readline()
            if not line:
                return
            if line.startswith('"NO"') or line.startswith("NO,"):
                f.seek(pos)
                break

        reader = csv.DictReader(f)
        for source_row_no, row in enumerate(reader, start=1):
            lease_type = clean(row.get(COL_LEASE_TYPE))
            if lease_type != JEONSE:
                continue

            region = clean(row.get(COL_REGION))
            sido, sigungu, eupmyeondong = split_region(region)
            area = row.get(COL_AREA) or row.get(COL_CONTRACT_AREA)
            ym = clean(row.get(COL_YM))
            day = clean(row.get(COL_DAY))

            yield (
                path.name,
                source_row_no,
                property_type,
                property_type_kr,
                region,
                sido,
                sigungu,
                eupmyeondong,
                clean(row.get(COL_JIBUN)),
                clean(row.get(COL_BONBUN)),
                clean(row.get(COL_BUBUN)),
                clean(row.get(COL_COMPLEX) or row.get(COL_BUILDING)),
                lease_type,
                decimal_value(area),
                ym,
                day,
                contract_date(ym, day),
                int_value(row.get(COL_DEPOSIT), 10000),
                int_value(row.get(COL_RENT), 10000),
                int_value(row.get(COL_FLOOR)),
                int_value(row.get(COL_BUILT_YEAR)),
                clean(row.get(COL_ROAD)),
                clean(row.get(COL_PERIOD)),
                clean(row.get(COL_CONTRACT_TYPE)),
                clean(row.get(COL_RENEWAL)),
                int_value(row.get(COL_PREV_DEPOSIT), 10000),
                int_value(row.get(COL_PREV_RENT), 10000),
                clean(row.get(COL_HOUSING_TYPE)),
                clean(row.get(COL_ROAD_CONDITION)),
            )


def load(data_dir):
    files = []
    for path in sorted(Path(data_dir).glob("*.csv")):
        detected = detect_type(path)
        if detected:
            files.append((path, *detected))

    if not files:
        raise SystemExit("No real rent transaction CSV files found.")

    with get_connection() as conn:
        conn.row_factory = dict_row
        with conn.cursor() as cur:
            cur.execute(DDL)
            total = 0
            for path, property_type, property_type_kr in files:
                cur.execute(
                    "DELETE FROM stg_real_rent_transactions WHERE source_file = %s",
                    (path.name,),
                )
                count = 0
                with cur.copy(COPY_SQL) as copy:
                    for row in iter_rows(path, property_type, property_type_kr):
                        copy.write_row(row)
                        count += 1
                total += count
                print(f"{path.name}\t{count}")
        conn.commit()

    print(f"TOTAL\t{total}")


if __name__ == "__main__":
    data_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    load(data_dir)
