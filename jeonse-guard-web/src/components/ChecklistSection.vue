<script setup>
import { ref } from "vue";
import { CheckCircle2 } from "@lucide/vue";

const checkedItems = ref(new Set());

const checklist = [
  "등기부등본 최신본 확인",
  "소유자와 계약자 일치 확인",
  "근저당권 확인",
  "압류/가압류 확인",
  "신탁등기 확인",
  "임차권등기명령 확인",
  "선순위 임차인 보증금 확인",
  "전세보증금반환보증 가입 가능 여부 확인",
  "건축물대장 확인",
  "공인중개사 등록 및 영업상태 확인",
  "잔금 전 등기부등본 재확인",
];

function toggleItem(item) {
  const next = new Set(checkedItems.value);

  if (next.has(item)) {
    next.delete(item);
  } else {
    next.add(item);
  }

  checkedItems.value = next;
}
</script>

<template>
  <section id="checklist" class="section">
    <div class="section-inner">
      <div class="section-heading">
        <p class="eyebrow">Checklist</p>
        <h2>전세사기 체크리스트</h2>
        <p>
          계약 전 확인할 서류와 질문을 빠뜨리지 않도록 핵심 항목을 정리했습니다.
        </p>
      </div>

      <div class="checklist-grid">
        <button
          v-for="item in checklist"
          :key="item"
          class="checklist-item"
          :class="{ checked: checkedItems.has(item) }"
          type="button"
          @click="toggleItem(item)"
        >
          <CheckCircle2 :size="20" aria-hidden="true" />
          <span>{{ item }}</span>
        </button>
      </div>
    </div>
  </section>
</template>
