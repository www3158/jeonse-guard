<script setup>
import { ClipboardList, FileText, Gauge, ShieldAlert } from "@lucide/vue";

const features = [
  {
    title: "AI 전세 위험 분석",
    description:
      "매물 데이터의 위험 요소를 정리하고 계약 전 추가 확인이 필요한 부분을 안내합니다.",
    icon: ShieldAlert,
  },
  {
    title: "보증금 조건 기반 매물 추천",
    description:
      "지역, 주택 유형, 최대 보증금 조건에 맞춰 우선 검토할 전세 후보를 보여줍니다.",
    icon: Gauge,
  },
  {
    title: "계약 전 질문 자동 생성",
    description:
      "중개사에게 확인해야 할 질문을 매물 위험 요소에 맞춰 준비합니다.",
    icon: ClipboardList,
  },
  {
    title: "특약 예시 제공",
    description:
      "계약 전 전문가 확인을 권장하는 특약 예시를 보기 쉽게 정리합니다.",
    icon: FileText,
  },
];
</script>

<template>
  <section id="service" class="section">
    <div class="section-inner">
      <div class="section-heading">
        <p class="eyebrow">Service</p>
        <h2>단순 매물 목록이 아닌 계약 전 확인 도구</h2>
        <p>
          전세가드 AI는 매물 선택 단계에서 위험 요소를 먼저 확인하도록 돕는
          포트폴리오 시연용 화면입니다.
        </p>
      </div>

      <div class="feature-grid">
        <article v-for="feature in features" :key="feature.title" class="feature-card">
          <component :is="feature.icon" :size="28" aria-hidden="true" />
          <h3>{{ feature.title }}</h3>
          <p>{{ feature.description }}</p>
        </article>
      </div>
    </div>
  </section>
</template>
