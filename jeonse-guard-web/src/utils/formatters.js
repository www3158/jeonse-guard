const propertyTypeLabels = {
  APT: "아파트",
  VILLA: "빌라",
  OFFICETEL: "오피스텔",
  SINGLE_MULTI: "단독/다가구",
};

const riskLevelLabels = {
  SAFE: "안전",
  CAUTION: "주의",
  WARNING: "주의",
  DANGER: "위험",
  safe: "안전",
  caution: "주의",
  warning: "주의",
  danger: "위험",
};

export function formatDeposit(value) {
  if (value === null || value === undefined || value === "") {
    return "보증금 확인 필요";
  }

  if (typeof value === "string" && Number.isNaN(Number(value.replace(/,/g, "")))) {
    return value;
  }

  const won = Number(String(value).replace(/,/g, ""));
  if (!Number.isFinite(won)) {
    return "보증금 확인 필요";
  }

  const manwon = Math.round(won / 10000);
  const eok = Math.floor(manwon / 10000);
  const remainder = manwon % 10000;

  if (eok > 0 && remainder > 0) {
    return `${eok}억 ${remainder.toLocaleString("ko-KR")}만원`;
  }

  if (eok > 0) {
    return `${eok}억원`;
  }

  return `${manwon.toLocaleString("ko-KR")}만원`;
}

export function formatArea(value) {
  if (value === null || value === undefined || value === "") {
    return "면적 확인 필요";
  }

  return `${Number(value).toLocaleString("ko-KR", {
    maximumFractionDigits: 1,
  })}㎡`;
}

export function formatFloor(value) {
  if (value === null || value === undefined || value === "") {
    return "층수 확인 필요";
  }

  if (typeof value === "string") {
    return value.includes("층") ? value : `${value}층`;
  }

  return `${value}층`;
}

export function formatStationDistance(value) {
  if (value === null || value === undefined || value === "") {
    return "역 거리 확인 필요";
  }

  return `역 도보 ${value}분`;
}

export function formatPropertyType(type) {
  return propertyTypeLabels[type] || type || "유형 확인 필요";
}

export function normalizeRiskLevel(level) {
  return riskLevelLabels[level] || level || "확인 필요";
}

export function getRiskClass(level) {
  const normalized = normalizeRiskLevel(level);

  if (normalized === "안전") {
    return "safe";
  }

  if (normalized === "주의") {
    return "caution";
  }

  if (normalized === "위험") {
    return "danger";
  }

  return "neutral";
}

export function formatScore(value) {
  if (value === null || value === undefined || value === "") {
    return "-";
  }

  const number = Number(value);
  return Number.isFinite(number) ? `${Math.round(number)}점` : String(value);
}

export function toArray(value) {
  if (Array.isArray(value)) {
    return value;
  }

  if (!value) {
    return [];
  }

  return [value];
}

export function createMailtoUrl(email, subject, body = "") {
  const params = new URLSearchParams({ subject });

  if (body.trim()) {
    params.set("body", body.trim());
  }

  return `mailto:${email}?${params.toString()}`;
}
