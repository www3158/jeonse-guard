<script setup>
import { ArrowRight, CheckCircle2, Search, ShieldCheck } from "@lucide/vue";

const emit = defineEmits(["navigate"]);
</script>

<template>
  <section id="hero" class="hero-section">
    <div class="hero-inner">
      <div class="hero-copy">
        <p class="eyebrow">AI Jeonse Risk Analysis</p>
        <h1>AI가 도와주는 안전한 전세 매물 선택</h1>
        <p class="hero-description">
          보증금, 지역, 권리관계 위험 요소를 분석해 전세사기 가능성을 낮추는
          매물 추천 서비스
        </p>
        <div class="hero-actions">
          <button class="primary-button" type="button" @click="emit('navigate', 'recommendations')">
            추천 매물 보기
            <ArrowRight :size="18" aria-hidden="true" />
          </button>
          <button class="secondary-button" type="button" @click="emit('navigate', 'checklist')">
            위험 체크하기
            <Search :size="18" aria-hidden="true" />
          </button>
        </div>
      </div>

      <div class="hero-dashboard" aria-label="전세 위험 분석 대시보드 예시">
        <div class="dashboard-topline">
          <span>분석 완료</span>
          <strong>92</strong>
        </div>
        <div class="mock-property-card">
          <div>
            <p>구로구 역세권 빌라</p>
            <strong>2억 5,000만원</strong>
          </div>
          <span class="risk-badge safe">안전</span>
        </div>
        <div class="risk-meter">
          <div class="risk-meter-row">
            <span>안전 점수</span>
            <strong>88점</strong>
          </div>
          <div class="meter-track">
            <span class="meter-fill"></span>
          </div>
        </div>
        <div class="badge-row">
          <span class="risk-badge safe">안전</span>
          <span class="risk-badge caution">주의</span>
          <span class="risk-badge danger">위험</span>
        </div>
        <div class="mini-insights">
          <div>
            <ShieldCheck :size="20" aria-hidden="true" />
            <span>권리관계 확인 필요</span>
          </div>
          <div>
            <CheckCircle2 :size="20" aria-hidden="true" />
            <span>계약 전 질문 생성</span>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
