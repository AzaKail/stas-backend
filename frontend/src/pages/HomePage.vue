<template>
  <div class="page">
    <HeaderBar @openMenu="menuOpen = true" />

    <div class="side" :class="{ open: menuOpen }" @click.self="menuOpen = false">
      <div class="side__panel">
        <div class="side__head">
          <div class="side__title">Меню</div>
          <button class="icon-btn" @click="menuOpen = false">✕</button>
        </div>
        <router-link class="side__link" to="/">Главная</router-link>
        <router-link class="side__link" to="/catalog">Каталог</router-link>
        <router-link class="side__link" to="/about">О нас</router-link>
        <router-link class="side__link" to="/sell">Продать</router-link>
      </div>
    </div>

    <main class="container">
      <section class="hero reveal">
        <h1>VVVStore — техника Apple и не только</h1>
        <p class="muted">
          Новые и б/у устройства, честное описание и помощь менеджера в Telegram.
        </p>
      </section>

      <section class="reveal">
        <div class="section-head">
          <h2>Главные категории</h2>
          <router-link class="muted small" to="/catalog">Смотреть каталог →</router-link>
        </div>

        <CategoryTabs :categories="categories" v-model="selectedCategory" />

        <div class="menu-grid" v-if="menuCards.length">
          <button
            v-for="(card, i) in menuCards"
            :key="card.slug"
            class="menu-card"
            :style="{ '--accent': cardColor(i) }"
            @click="goToCategory(card.slug)"
          >
            <div class="menu-card__media">
              <span class="menu-card__icon"></span>
            </div>
            <div class="menu-card__content">
              <div class="menu-card__title">{{ card.title }}</div>
              <div class="menu-card__text">Подборка устройств и аксессуаров</div>
            </div>
          </button>
        </div>
      </section>

      <section class="sell-cta reveal">
        <div>
          <h3>Продайте своё устройство</h3>
          <p class="muted">
            Оставьте заявку — мы свяжемся, оценим устройство и добавим его в каталог.
          </p>
        </div>
        <router-link class="btn" to="/sell">Продать своё</router-link>
      </section>

      <section class="reveal">
        <div class="section-head">
          <h2>Случайные товары</h2>
          <button class="btn btn--ghost" @click="loadFeatured">Обновить</button>
        </div>

        <div class="grid">
          <div v-if="loading" v-for="i in 6" :key="i" class="skeleton"></div>
          <ProductCard v-else v-for="p in featured" :key="p.id" :item="p" />
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from "vue";
import { useRouter } from "vue-router";
import HeaderBar from "../components/HeaderBar.vue";
import CategoryTabs from "../components/CategoryTabs.vue";
import ProductCard from "../components/ProductCard.vue";
import { api } from "../api";
import { useCatalogStore } from "../stores/catalog";

const menuOpen = ref(false);
const selectedCategory = ref("");
const featured = ref([]);
const loading = ref(false);

const store = useCatalogStore();
const router = useRouter();

const categories = computed(() => store.categories || []);
const menuCards = computed(() => categories.value.slice(0, 8));

const colors = ["#e5e7eb", "#dbeafe", "#fce7f3", "#ecfccb", "#ede9fe", "#d1fae5"];
const cardColor = (index) => colors[index % colors.length];

function shuffle(arr) {
  const copy = [...arr];
  for (let i = copy.length - 1; i > 0; i -= 1) {
    const j = Math.floor(Math.random() * (i + 1));
    [copy[i], copy[j]] = [copy[j], copy[i]];
  }
  return copy;
}

async function loadFeatured() {
  loading.value = true;
  try {
    const params = {};
    if (selectedCategory.value) params.category = selectedCategory.value;
    const res = await api.get("products/", { params });
    const items = res.data.results ?? res.data;
    featured.value = shuffle(items).slice(0, 6);
  } finally {
    loading.value = false;
  }
}

function goToCategory(slug) {
  store.category = slug;
  router.push("/catalog");
}

onMounted(async () => {
  await store.loadCategories();
  await loadFeatured();

  const els = document.querySelectorAll(".reveal");
  const io = new IntersectionObserver(
    (entries) => entries.forEach((e) => e.isIntersecting && e.target.classList.add("in")),
    { threshold: 0.12 }
  );
  els.forEach((el) => io.observe(el));
});

watch(selectedCategory, () => {
  loadFeatured();
});
</script>