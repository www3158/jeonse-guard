<script setup>
import { computed, reactive } from "vue";
import { Mail, MessageCircle, Send } from "@lucide/vue";
import {
  CONTACT_EMAIL,
  KAKAO_OPENCHAT_URL,
} from "../api/propertyApi";
import { createMailtoUrl } from "../utils/formatters";

const form = reactive({
  name: "",
  email: "",
  message: "",
});

const quickMailto = computed(() =>
  createMailtoUrl(CONTACT_EMAIL, "전세가드 AI 문의"),
);

const formMailto = computed(() => {
  const body = [
    form.name ? `이름: ${form.name}` : "",
    form.email ? `이메일: ${form.email}` : "",
    form.message ? `문의 내용:\n${form.message}` : "",
  ]
    .filter(Boolean)
    .join("\n\n");

  return createMailtoUrl(CONTACT_EMAIL, "전세가드 AI 문의", body);
});
</script>

<template>
  <section id="contact" class="section contact-section">
    <div class="section-inner contact-layout">
      <div class="contact-copy">
        <p class="eyebrow">Contact</p>
        <h2>계약 전, 한 번 더 확인하세요</h2>
        <p>
          전세가드 AI는 매물 데이터를 기반으로 위험 요소를 정리해주지만,
          최종 계약 전에는 반드시 전문가와 서류 확인이 필요합니다.
        </p>
        <div class="contact-actions">
          <a class="primary-button" :href="KAKAO_OPENCHAT_URL" target="_blank" rel="noreferrer">
            <MessageCircle :size="18" aria-hidden="true" />
            카카오톡 오픈채팅 문의
          </a>
          <a class="secondary-button" :href="quickMailto">
            <Mail :size="18" aria-hidden="true" />
            메일로 문의하기
          </a>
        </div>
      </div>

      <form class="contact-form">
        <label>
          <span>이름</span>
          <input v-model="form.name" placeholder="홍길동" />
        </label>
        <label>
          <span>이메일</span>
          <input v-model="form.email" type="email" placeholder="name@example.com" />
        </label>
        <label>
          <span>문의 내용</span>
          <textarea v-model="form.message" rows="5" placeholder="확인하고 싶은 매물이나 계약 상황을 적어주세요."></textarea>
        </label>
        <a class="primary-button contact-submit" :href="formMailto">
          <Send :size="18" aria-hidden="true" />
          메일 앱으로 문의하기
        </a>
      </form>
    </div>
  </section>
</template>
