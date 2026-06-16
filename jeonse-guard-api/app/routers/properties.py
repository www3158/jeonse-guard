from fastapi import APIRouter, HTTPException
from app.database import get_connection

router = APIRouter(prefix="/api/properties", tags=["properties"])


@router.get("")
def get_properties():
    sql = """
        SELECT
            p.id,
            p.external_property_id,
            p.title,
            p.address,
            p.region,
            p.lawd_cd,
            p.property_type,
            p.deposit,
            p.monthly_rent,
            p.area_m2,
            p.floor,
            p.maintenance_fee,
            p.station_distance_min,
            p.move_in_date,
            p.risk_level,
            p.risk_tags,
            r.risk_score,
            r.has_mortgage,
            r.has_seizure,
            r.has_provisional_seizure,
            r.has_trust,
            r.has_leasehold_registration,
            r.insurance_checked,
            r.senior_tenant_checked,
            r.building_register_checked,
            r.broker_status_checked
        FROM properties p
        LEFT JOIN property_risk_checks r
            ON p.id = r.property_id
        ORDER BY p.id;
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            rows = cur.fetchall()

    return {
        "count": len(rows),
        "items": rows
    }


@router.get("/{property_id}")
def get_property(property_id: int):
    sql = """
        SELECT
            p.id,
            p.external_property_id,
            p.title,
            p.address,
            p.region,
            p.lawd_cd,
            p.property_type,
            p.deposit,
            p.monthly_rent,
            p.area_m2,
            p.floor,
            p.maintenance_fee,
            p.station_distance_min,
            p.move_in_date,
            p.risk_level,
            p.risk_tags,
            r.risk_score,
            r.has_mortgage,
            r.has_seizure,
            r.has_provisional_seizure,
            r.has_trust,
            r.has_leasehold_registration,
            r.insurance_checked,
            r.senior_tenant_checked,
            r.building_register_checked,
            r.broker_status_checked
        FROM properties p
        LEFT JOIN property_risk_checks r
            ON p.id = r.property_id
        WHERE p.id = %s;
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (property_id,))
            row = cur.fetchone()

    if row is None:
        raise HTTPException(status_code=404, detail="매물을 찾을 수 없습니다.")

    return row