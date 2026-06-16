<script setup>
import { Building2, MapPin, ShieldCheck } from "@lucide/vue";
import { getPropertyId } from "../api/propertyApi";
import {
  formatArea,
  formatDeposit,
  formatFloor,
  formatPropertyType,
  formatScore,
  formatStationDistance,
  getRiskClass,
  normalizeRiskLevel,
  toArray,
} from "../utils/formatters";

const props = defineProps({
  property: {
    type: Object,
    required: true,
  },
  recommendation: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(["analyze"]);
</script>

<template>
  <article class="property-card">
    <div class="property-card-header">
      <div>
        <p class="property-type">{{ formatPropertyType(property.property_type) }}</p>
        <h3>{{ property.title || "매물명 확인 필요" }}</h3>
      </div>
      <span class="risk-badge" :class="getRiskClass(property.risk_level)">
        {{ normalizeRiskLevel(property.risk_level) }}
      </span>
    </div>

    <p class="property-address">
      <MapPin :size="16" aria-hidden="true" />
      {{ property.address || property.region || "주소 확인 필요" }}
    </p>

    <dl class="property-meta">
      <div>
        <dt>보증금</dt>
        <dd>{{ formatDeposit(property.deposit) }}</dd>
      </div>
      <div>
        <dt>면적</dt>
        <dd>{{ formatArea(property.area_m2) }}</dd>
      </div>
      <div>
        <dt>층수</dt>
        <dd>{{ formatFloor(property.floor) }}</dd>
      </div>
      <div>
        <dt>역 거리</dt>
        <dd>{{ formatStationDistance(property.station_distance_min) }}</dd>
      </div>
    </dl>

    <div class="score-strip">
      <div v-if="recommendation && property.final_score !== undefined">
        <span>추천 점수</span>
        <strong>{{ formatScore(property.final_score) }}</strong>
      </div>
      <div>
        <span>위험 점수</span>
        <strong>{{ formatScore(property.risk_score) }}</strong>
      </div>
    </div>

    <div v-if="recommendation" class="score-grid">
      <div>
        <span>안전 점수</span>
        <strong>{{ formatScore(property.safety_score) }}</strong>
      </div>
      <div>
        <span>교통 점수</span>
        <strong>{{ formatScore(property.transport_score) }}</strong>
      </div>
      <div>
        <span>예산 점수</span>
        <strong>{{ formatScore(property.budget_score) }}</strong>
      </div>
    </div>

    <div v-if="toArray(property.risk_tags).length" class="tag-row">
      <span v-for="tag in toArray(property.risk_tags)" :key="tag">{{ tag }}</span>
    </div>

    <button
      class="card-action"
      type="button"
      :disabled="!getPropertyId(property)"
      @click="emit('analyze', property)"
    >
      <ShieldCheck :size="18" aria-hidden="true" />
      상세 위험 분석
    </button>

    <Building2 class="property-watermark" :size="96" aria-hidden="true" />
  </article>
</template>
