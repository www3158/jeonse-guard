<script setup>
import { MessageCircle } from "@lucide/vue";
import { KAKAO_OPENCHAT_URL } from "../api/propertyApi";

const emit = defineEmits(["navigate"]);

const menuItems = [
  { label: "서비스 소개", target: "service" },
  { label: "추천 매물", target: "recommendations" },
  { label: "매물 보기", target: "properties" },
  { label: "위험 체크", target: "checklist" },
  { label: "문의하기", target: "contact" },
];

function openKakao() {
  window.open(KAKAO_OPENCHAT_URL, "_blank", "noopener,noreferrer");
}
</script>

<template>
  <header class="site-header">
    <div class="header-inner">
      <button class="brand-button" type="button" @click="emit('navigate', 'hero')">
        <span class="brand-mark">JG</span>
        <span>전세가드 AI</span>
      </button>

      <nav class="header-nav" aria-label="주요 메뉴">
        <button
          v-for="item in menuItems"
          :key="item.target"
          type="button"
          @click="emit('navigate', item.target)"
        >
          {{ item.label }}
        </button>
      </nav>

      <button class="header-cta" type="button" @click="openKakao">
        <MessageCircle :size="18" aria-hidden="true" />
        카카오톡 상담
      </button>
    </div>
  </header>
</template>
