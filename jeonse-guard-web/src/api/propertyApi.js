export const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";
export const KAKAO_OPENCHAT_URL =
  import.meta.env.VITE_KAKAO_OPENCHAT_URL || "https://open.kakao.com/o/g7TDr4yi";
export const CONTACT_EMAIL =
  import.meta.env.VITE_CONTACT_EMAIL || "last5324@gmail.com";

export const API_ERROR_MESSAGE =
  "데이터를 불러오지 못했습니다. FastAPI 서버와 Docker DB 실행 상태를 확인해주세요.";

function normalizeList(payload) {
  if (Array.isArray(payload)) {
    return payload;
  }

  const possibleKeys = ["items", "data", "results", "properties", "recommendations"];
  for (const key of possibleKeys) {
    if (Array.isArray(payload?.[key])) {
      return payload[key];
    }
  }

  return [];
}

async function request(path) {
  const response = await fetch(`${API_BASE_URL}${path}`);

  if (!response.ok) {
    throw new Error(API_ERROR_MESSAGE);
  }

  return response.json();
}

export function getPropertyId(property) {
  return (
    property?.id ??
    property?.property_id ??
    property?.propertyId ??
    property?.uuid ??
    null
  );
}

export function buildRecommendationQuery(filters) {
  const params = new URLSearchParams();
  const region = filters.region?.trim();
  const propertyType = filters.property_type;
  const maxDeposit = String(filters.max_deposit || "").replace(/[^\d]/g, "");

  if (region) {
    params.set("region", region);
  }

  if (propertyType) {
    params.set("property_type", propertyType);
  }

  if (maxDeposit) {
    params.set("max_deposit", maxDeposit);
  }

  const query = params.toString();
  return query ? `?${query}` : "";
}

export async function getProperties() {
  const payload = await request("/api/properties");
  return normalizeList(payload).slice(0, 50);
}

export async function getRecommendations(filters = {}) {
  const payload = await request(
    `/api/recommendations${buildRecommendationQuery(filters)}`,
  );
  return normalizeList(payload);
}

export async function getRiskAnalysis(propertyId) {
  return request(`/api/properties/${propertyId}/analysis`);
}
