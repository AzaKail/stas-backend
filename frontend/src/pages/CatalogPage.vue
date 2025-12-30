<template>
  <div class="page">
    <HeaderBar @openMenu="menuOpen = true" />

    <!-- простое левое меню (mobile/desktop) -->
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
        <h1>Каталог техники</h1>
        <p class="muted">Фильтры работают по вариантам (память/цвет) и тэгам.</p>
      </section>

      <section class="reveal">
        <CategoryTabs :categories="store.categories" v-model="store.category" />

        <div class="toolbar">
          <input
            class="input"
            placeholder="Поиск…"
            v-model="store.q"
            @input="debouncedSearch"
          />
          <button class="btn" @click="filtersOpen = true">Фильтры</button>
          <button class="btn btn--ghost" @click="resetAll">Сброс</button>
        </div>

        <div class="chips" v-if="activeChips.length">
          <button class="chip" v-for="c in activeChips" :key="c.key" @click="c.remove()">
            {{ c.label }} ✕
          </button>
        </div>

        <div class="grid">
          <div v-if="store.loading" v-for="i in 12" :key="i" class="skeleton"></div>

          <ProductCard v-else v-for="p in store.items" :key="p.id" :item="p" />
        </div>

        <div class="muted small" style="margin-top: 12px;">
          Найдено: {{ store.count }}
        </div>

        <div class="pager" v-if="pages > 1">
          <button class="btn btn--ghost" :disabled="store.page <= 1" @click="go(store.page - 1)">
            ←
          </button>
          <div class="muted">Стр. {{ store.page }} / {{ pages }}</div>
          <button class="btn btn--ghost" :disabled="store.page >= pages" @click="go(store.page + 1)">
            →
          </button>
        </div>
      </section>
    </main>

    <FilterDrawer
      :open="filtersOpen"
      :meta="store.filtersMeta"
      :value="{
        memories: store.memories,
        colors: store.colors,
        tags: store.tags,
        priceMin: store.priceMin,
        priceMax: store.priceMax,
      }"
      @close="filtersOpen = false"
      @apply="applyFilters"
      @reset="resetAll"
    />
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from "vue";
import HeaderBar from "../components/HeaderBar.vue";
import CategoryTabs from "../components/CategoryTabs.vue";
import FilterDrawer from "../components/FilterDrawer.vue";
import ProductCard from "../components/ProductCard.vue";
import { useCatalogStore } from "../stores/catalog";

const store = useCatalogStore();

const filtersOpen = ref(false);
const menuOpen = ref(false);

let t = null;
function debouncedSearch() {
  clearTimeout(t);
  t = setTimeout(() => {
    store.page = 1;
    store.loadProducts();
  }, 300);
}

function applyFilters(v) {
  store.memories = v.memories;
  store.colors = v.colors;
  store.tags = v.tags;
  store.priceMin = v.priceMin;
  store.priceMax = v.priceMax;
  store.page = 1;
  store.loadProducts();
}

function resetAll() {
  store.resetFilters();
  store.loadProducts();
}

function go(p) {
  store.page = p;
  store.loadProducts();
}

const pages = computed(() => Math.ceil((store.count || 0) / store.pageSize));

const tagLabels = computed(() => {
  const map = {};
  (store.filtersMeta.tags || []).forEach((t) => {
    const slug = t.slug || t;
    const title = t.title || t;
    if (slug) map[slug] = title;
  });
  return map;
});

const activeChips = computed(() => {
  const chips = [];

  store.memories.forEach((m) =>
    chips.push({ key: "m" + m, label: `${m}GB`, remove: () => (store.memories = store.memories.filter(x => x !== m), store.loadProducts()) })
  );
  store.colors.forEach((c) =>
    chips.push({ key: "c" + c, label: c, remove: () => (store.colors = store.colors.filter(x => x !== c), store.loadProducts()) })
  );
  store.tags.forEach((tg) => {
    const label = tagLabels.value[tg] || tg;
    chips.push({
      key: "t" + tg,
      label: `#${label}`,
      remove: () => ((store.tags = store.tags.filter((x) => x !== tg)), store.loadProducts()),
    });
  });

  if (store.priceMin !== null || store.priceMax !== null) {
    chips.push({
      key: "price",
      label: `Цена: ${store.priceMin}–${store.priceMax}`,
      remove: () => {
        store.priceMin = store.filtersMeta.price.min;
        store.priceMax = store.filtersMeta.price.max;
        store.loadProducts();
      },
    });
  }

  return chips;
});

onMounted(async () => {
  await store.loadCategories();
  await store.loadFiltersMeta();
  await store.loadProducts();

  // анимация появления при скролле
  const els = document.querySelectorAll(".reveal");
  const io = new IntersectionObserver(
    (entries) => entries.forEach((e) => e.isIntersecting && e.target.classList.add("in")),
    { threshold: 0.12 }
  );
  els.forEach((el) => io.observe(el));
});

// при смене категории — перезагрузим фильтры + товары
watch(
  () => store.category,
  async () => {
    store.page = 1;
    store.memories = [];
    store.colors = [];
    store.tags = [];
    await store.loadFiltersMeta();
    await store.loadProducts();
  }
);
</script>
