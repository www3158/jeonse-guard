<script setup>
import { onMounted, reactive, ref } from "vue";
import { Filter, RefreshCw } from "@lucide/vue";
import { API_ERROR_MESSAGE, getRecommendations, getPropertyId } from "../api/propertyApi";
import PropertyCard from "./PropertyCard.vue";

const emit = defineEmits(["analyze"]);

const filters = reactive({
  region: "",
  property_type: "",
  max_deposit: "",
});
const recommendations = ref([]);
const loading = ref(false);
const error = ref("");

async function loadRecommendations() {
  loading.value = true;
  error.value = "";

  try {
    recommendations.value = await getRecommendations(filters);
  } catch {
    error.value = API_ERROR_MESSAGE;
    recommendations.value = [];
  } finally {
    loading.value = false;
  }
}

onMounted(loadRecommendations);
</script>

<template>
  <section id="recommendations" class="section section-muted">
    <div class="section-inner">
      <div class="section-heading">
        <p class="eyebrow">Recommendations</p>
        <h2>조건에 맞는 추천 매물</h2>
        <p>
          지역과 예산 조건을 입력하면 FastAPI 추천 API를 호출해 후보 매물을
          정리합니다.
        </p>
      </div>

      <form class="filter-panel" @submit.prevent="loadRecommendations">
        <label>
          <span>지역 검색</span>
          <input v-model="filters.region" type="search" placeholder="예: 구로구" />
        </label>
        <label>
          <span>주택 유형</span>
          <select v-model="filters.property_type">
            <option value="">전체</option>
            <option value="APT">APT</option>
            <option value="VILLA">VILLA</option>
            <option value="OFFICETEL">OFFICETEL</option>
            <option value="SINGLE_MULTI">SINGLE_MULTI</option>
          </select>
        </label>
        <label>
          <span>최대 보증금</span>
          <input
            v-model="filters.max_deposit"
            inputmode="numeric"
            placeholder="예: 250000000"
          />
        </label>
        <button class="primary-button filter-button" type="submit" :disabled="loading">
          <RefreshCw v-if="loading" :size="18" aria-hidden="true" />
          <Filter v-else :size="18" aria-hidden="true" />
          추천 조회
        </button>
      </form>

      <div v-if="loading" class="state-card">불러오는 중...</div>
      <div v-else-if="error" class="state-card state-error">{{ error }}</div>
      <div v-else-if="recommendations.length === 0" class="state-card">
        조건에 맞는 매물이 없습니다. 필터를 조정해주세요.
      </div>
      <div v-else class="property-grid recommendation-grid">
        <PropertyCard
          v-for="property in recommendations"
          :key="getPropertyId(property) || property.title || property.address"
          :property="property"
          recommendation
          @analyze="emit('analyze', property)"
        />
      </div>
    </div>
  </section>
</template>
