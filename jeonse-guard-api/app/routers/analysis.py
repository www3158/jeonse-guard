from fastapi import APIRouter, HTTPException
from app.database import get_connection

router = APIRouter(prefix="/api/properties", tags=["analysis"])


@router.get("/{property_id}/analysis")
def analyze_property(property_id: int):
    sql = """
        SELECT
            p.id,
            p.title,
            p.address,
            p.region,
            p.property_type,
            p.deposit,
            p.risk_level,
            p.risk_tags,
            r.risk_score,
            r.has_mortgage,
            r.has_seizure,
            r.has_provisional_seizure,
            r.has_trust,
            r.has_leasehold_registration,
            r.owner_matched,
            r.insurance_checked,
            r.senior_tenant_checked,
            r.building_register_checked,
            r.broker_status_checked,
            r.registry_checked_before_balance
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

    risk_reasons = []
    questions_to_broker = []
    special_clause_examples = []

    if row["has_mortgage"]:
        risk_reasons.append("근저당이 있어 선순위 권리와 채권최고액 확인이 필요합니다.")
        questions_to_broker.append("근저당 채권최고액은 얼마인가요?")
        special_clause_examples.append("잔금 전까지 근저당 말소가 완료되지 않을 경우 계약을 해제할 수 있다.")

    if row["has_seizure"]:
        risk_reasons.append("압류가 확인되어 보증금 반환 위험이 높습니다.")
        questions_to_broker.append("압류가 발생한 사유와 해제 예정일을 확인할 수 있나요?")
        special_clause_examples.append("압류 해제가 확인되지 않을 경우 계약은 무효로 한다.")

    if row["has_provisional_seizure"]:
        risk_reasons.append("가압류가 확인되어 권리관계 확인이 필요합니다.")
        questions_to_broker.append("가압류 해제 가능 여부와 관련 서류를 확인할 수 있나요?")

    if row["has_trust"]:
        risk_reasons.append("신탁등기가 있어 임대 권한 확인이 반드시 필요합니다.")
        questions_to_broker.append("신탁회사 동의서 또는 임대 권한 증빙을 확인할 수 있나요?")
        special_clause_examples.append("신탁회사의 임대차 동의가 확인되지 않을 경우 계약을 진행하지 않는다.")

    if row["has_leasehold_registration"]:
        risk_reasons.append("임차권등기명령 이력이 있어 이전 임차인의 보증금 반환 문제가 있었을 가능성이 있습니다.")
        questions_to_broker.append("임차권등기명령 발생 사유와 말소 여부를 확인할 수 있나요?")

    if row["owner_matched"] is False:
        risk_reasons.append("소유자와 계약자가 일치하지 않아 대리계약 위험이 있습니다.")
        questions_to_broker.append("소유자의 위임장과 인감증명서를 확인할 수 있나요?")

    if row["insurance_checked"] is False:
        risk_reasons.append("전세보증금반환보증 가입 가능 여부가 확인되지 않았습니다.")
        questions_to_broker.append("HUG 전세보증금반환보증 가입이 가능한 매물인가요?")

    if row["senior_tenant_checked"] is False:
        risk_reasons.append("선순위 임차인 정보가 확인되지 않았습니다.")
        questions_to_broker.append("선순위 임차인의 보증금 총액을 확인할 수 있나요?")

    if row["building_register_checked"] is False:
        risk_reasons.append("건축물대장 확인이 필요합니다.")
        questions_to_broker.append("건축물대장상 용도와 실제 사용 용도가 일치하나요?")

    if row["broker_status_checked"] is False:
        risk_reasons.append("중개업소 영업 상태 확인이 필요합니다.")
        questions_to_broker.append("공인중개사 등록번호와 보증보험 가입 여부를 확인할 수 있나요?")

    if row["registry_checked_before_balance"] is False:
        risk_reasons.append("잔금 전 등기부등본 재확인이 필요합니다.")
        questions_to_broker.append("잔금 당일 최신 등기부등본을 다시 확인할 수 있나요?")
        special_clause_examples.append("잔금일 등기부등본상 새로운 권리침해가 확인될 경우 계약을 해제할 수 있다.")

    if not risk_reasons:
        risk_reasons.append("현재 데이터 기준으로 큰 위험 요소는 확인되지 않았습니다.")
        questions_to_broker.append("계약 전 최신 등기부등본과 건축물대장을 다시 확인할 수 있나요?")

    if row["risk_score"] >= 80:
        summary = "이 매물은 전세사기 위험 요소가 많이 확인되어 신중한 검토가 필요합니다."
    elif row["risk_score"] >= 30:
        summary = "이 매물은 일부 위험 요소가 있어 계약 전 추가 확인이 필요합니다."
    else:
        summary = "이 매물은 현재 데이터 기준으로 비교적 안전한 편입니다."

    return {
        "property_id": row["id"],
        "title": row["title"],
        "address": row["address"],
        "region": row["region"],
        "property_type": row["property_type"],
        "deposit": row["deposit"],
        "risk_level": row["risk_level"],
        "risk_score": row["risk_score"],
        "risk_tags": row["risk_tags"],
        "summary": summary,
        "risk_reasons": risk_reasons,
        "questions_to_broker": questions_to_broker,
        "special_clause_examples": special_clause_examples
    }