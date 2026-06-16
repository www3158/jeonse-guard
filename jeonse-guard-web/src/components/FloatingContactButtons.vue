<script setup>
import { Home, Mail, MessageCircle } from "@lucide/vue";
import {
  CONTACT_EMAIL,
  KAKAO_OPENCHAT_URL,
} from "../api/propertyApi";
import { createMailtoUrl } from "../utils/formatters";

const emit = defineEmits(["navigate"]);
const mailtoUrl = createMailtoUrl(CONTACT_EMAIL, "전세가드 AI 문의");
</script>

<template>
  <div class="floating-actions" aria-label="빠른 상담 버튼">
    <a :href="KAKAO_OPENCHAT_URL" target="_blank" rel="noreferrer">
      <MessageCircle :size="18" aria-hidden="true" />
      <span>카카오톡 상담</span>
    </a>
    <a :href="mailtoUrl">
      <Mail :size="18" aria-hidden="true" />
      <span>메일 문의</span>
    </a>
    <button type="button" @click="emit('navigate', 'recommendations')">
      <Home :size="18" aria-hidden="true" />
      <span>추천 매물 보기</span>
    </button>
  </div>
</template>
