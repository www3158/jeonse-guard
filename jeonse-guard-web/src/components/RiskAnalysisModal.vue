<script setup>
import { computed, watch } from "vue";
import { X } from "@lucide/vue";
import {
  formatDeposit,
  formatScore,
  getRiskClass,
  normalizeRiskLevel,
  toArray,
} from "../utils/formatters";

const props = defineProps({
  open: {
    type: Boolean,
    required: true,
  },
  analysis: {
    type: Object,
    default: null,
  },
  fallbackProperty: {
    type: Object,
    default: null,
  },
  loading: {
    type: Boolean,
    default: false,
  },
  error: {
    type: String,
    default: "",
  },
});

const emit = defineEmits(["close"]);

const displayData = computed(() => ({
  ...(props.fallbackProperty || {}),
  ...(props.analysis || {}),
}));

function handleKeydown(event) {
  if (event.key === "Escape" && props.open) {
    emit("close");
  }
}

watch(
  () => props.open,
  (isOpen) => {
    if (isOpen) {
      document.addEventListener("keydown", handleKeydown);
      document.body.classList.add("modal-open");
    } else {
      document.removeEventListener("keydown", handleKeydown);
      document.body.classList.remove("modal-open");
    }
  },
);
</script>

<template>
  <Teleport to="body">
    <div v-if="open" class="modal-backdrop" @click.self="emit('close')">
      <section class="analysis-modal" aria-modal="true" role="dialog">
        <button class="modal-close" type="button" aria-label="모달 닫기" @click="emit('close')">
          <X :size="22" aria-hidden="true" />
        </button>

        <div v-if="loading" class="state-card">불러오는 중...</div>
        <div v-else-if="error" class="state-card state-error">{{ error }}</div>
        <template v-else>
          <div class="modal-header">
            <div>
              <p class="eyebrow">Risk Analysis</p>
              <h2>{{ displayData.title || "매물명 확인 필요" }}</h2>
              <p>{{ displayData.address || "주소 확인 필요" }}</p>
            </div>
            <span class="risk-badge" :class="getRiskClass(displayData.risk_level)">
              {{ normalizeRiskLevel(displayData.risk_level) }}
            </span>
          </div>

          <div class="analysis-summary">
            <div>
              <span>보증금</span>
              <strong>{{ formatDeposit(displayData.deposit) }}</strong>
            </div>
            <div>
              <span>위험 점수</span>
              <strong>{{ formatScore(displayData.risk_score) }}</strong>
            </div>
          </div>

          <section class="modal-section">
            <h3>요약</h3>
            <p>
              {{
                displayData.summary ||
                "현재 데이터 기준으로 확인이 필요한 위험 요소를 정리합니다."
              }}
            </p>
          </section>

          <section v-if="toArray(displayData.risk_reasons).length" class="modal-section">
            <h3>위험 사유</h3>
            <div class="reason-list">
              <article
                v-for="reason in toArray(displayData.risk_reasons)"
                :key="reason"
                class="reason-card"
              >
                {{ reason }}
              </article>
            </div>
          </section>

          <section v-if="toArray(displayData.questions_to_broker).length" class="modal-section">
            <h3>중개사에게 물어볼 질문</h3>
            <ul class="clean-list">
              <li v-for="question in toArray(displayData.questions_to_broker)" :key="question">
                {{ question }}
              </li>
            </ul>
          </section>

          <section
            v-if="toArray(displayData.special_clause_examples).length"
            class="modal-section"
          >
            <h3>특약 예시</h3>
            <div class="clause-box">
              <p
                v-for="clause in toArray(displayData.special_clause_examples)"
                :key="clause"
              >
                {{ clause }}
              </p>
            </div>
          </section>

          <div v-if="toArray(displayData.risk_tags).length" class="tag-row">
            <span v-for="tag in toArray(displayData.risk_tags)" :key="tag">{{ tag }}</span>
          </div>
        </template>
      </section>
    </div>
  </Teleport>
</template>
