<script setup>
import { onMounted, ref } from "vue";
import HeaderNav from "./components/HeaderNav.vue";
import HeroSection from "./components/HeroSection.vue";
import ServiceIntroSection from "./components/ServiceIntroSection.vue";
import RecommendationSection from "./components/RecommendationSection.vue";
import PropertyCard from "./components/PropertyCard.vue";
import RiskAnalysisModal from "./components/RiskAnalysisModal.vue";
import ChecklistSection from "./components/ChecklistSection.vue";
import ContactSection from "./components/ContactSection.vue";
import FloatingContactButtons from "./components/FloatingContactButtons.vue";
import {
  API_ERROR_MESSAGE,
  getProperties,
  getPropertyId,
  getRiskAnalysis,
} from "./api/propertyApi";

const properties = ref([]);
const propertiesLoading = ref(false);
const propertiesError = ref("");
const analysisOpen = ref(false);
const analysis = ref(null);
const analysisLoading = ref(false);
const analysisError = ref("");
const selectedProperty = ref(null);

function scrollToSection(sectionId) {
  document.getElementById(sectionId)?.scrollIntoView({
    behavior: "smooth",
    block: "start",
  });
}

async function loadProperties() {
  propertiesLoading.value = true;
  propertiesError.value = "";

  try {
    properties.value = await getProperties();
  } catch {
    propertiesError.value = API_ERROR_MESSAGE;
  } finally {
    propertiesLoading.value = false;
  }
}

async function openAnalysis(property) {
  const propertyId = getPropertyId(property);

  if (!propertyId) {
    selectedProperty.value = property;
    analysis.value = null;
    analysisError.value = "매물 식별값을 확인할 수 없습니다.";
    analysisOpen.value = true;
    return;
  }

  selectedProperty.value = property;
  analysisOpen.value = true;
  analysisLoading.value = true;
  analysisError.value = "";
  analysis.value = null;

  try {
    analysis.value = await getRiskAnalysis(propertyId);
  } catch {
    analysisError.value = API_ERROR_MESSAGE;
  } finally {
    analysisLoading.value = false;
  }
}

function closeAnalysis() {
  analysisOpen.value = false;
}

onMounted(loadProperties);
</script>

<template>
  <HeaderNav @navigate="scrollToSection" />

  <main>
    <HeroSection @navigate="scrollToSection" />
    <ServiceIntroSection />
    <RecommendationSection @analyze="openAnalysis" />

    <section id="properties" class="section section-muted">
      <div class="section-inner">
        <div class="section-heading">
          <p class="eyebrow">Property List</p>
          <h2>전체 매물 보기</h2>
          <p>
            FastAPI 매물 목록과 연결해 최대 50개의 전세 후보를 카드로 확인합니다.
          </p>
        </div>

        <div v-if="propertiesLoading" class="state-card">불러오는 중...</div>
        <div v-else-if="propertiesError" class="state-card state-error">
          {{ propertiesError }}
        </div>
        <div v-else-if="properties.length === 0" class="state-card">
          조건에 맞는 매물이 없습니다. 필터를 조정해주세요.
        </div>
        <div v-else class="property-grid">
          <PropertyCard
            v-for="property in properties"
            :key="getPropertyId(property) || property.title || property.address"
            :property="property"
            @analyze="openAnalysis"
          />
        </div>
      </div>
    </section>

    <ChecklistSection />
    <ContactSection />
  </main>

  <FloatingContactButtons @navigate="scrollToSection" />
  <RiskAnalysisModal
    :open="analysisOpen"
    :analysis="analysis"
    :fallback-property="selectedProperty"
    :loading="analysisLoading"
    :error="analysisError"
    @close="closeAnalysis"
  />
</template>
