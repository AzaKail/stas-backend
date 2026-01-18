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
      <router-link class="muted small" to="/catalog">← Назад в каталог</router-link>

      <section class="hero" v-if="loading">
        <p class="muted">Загружаем товар…</p>
      </section>

      <section class="hero" v-else-if="error">
        <p class="muted">{{ error }}</p>
      </section>

      <section v-else class="product">
        <div>
          <div class="product__img card">
            <img v-if="cover" :src="cover" :alt="product.title" />
            <div v-else class="ph" />
          </div>
        </div>

        <div>
          <h1>{{ product.title }}</h1>
          <div class="muted small" style="margin: 6px 0 12px;">
            <span v-if="product.brand">Бренд: {{ product.brand }}</span>
            <span v-if="product.warranty"> · {{ product.warranty }}</span>
          </div>
          <p class="muted" v-if="product.description" style="line-height: 1.5;">{{ product.description }}</p>

          <div class="filter-block" v-if="tags.length" style="padding-top:6px;">
            <div class="label">Тэги</div>
            <div class="chips">
              <button class="chip" v-for="t in tags" :key="t.slug" @click="goToTag(t.slug)">
                #{{ t.title }}
              </button>
            </div>
          </div>

          <div class="filter-block" v-if="memories.length">
            <div class="label">Память</div>
            <div class="chips">
              <button
                v-for="m in memories"
                :key="m"
                class="chip"
                :class="{ active: selectedMemory === m }"
                @click="selectMemory(m)"
              >
                {{ m }}GB
              </button>
            </div>
          </div>

          <div class="filter-block" v-if="colors.length">
            <div class="label">Цвет</div>
            <div class="chips">
              <button
                v-for="c in colors"
                :key="c"
                class="chip"
                :class="{ active: selectedColor === c }"
                @click="selectColor(c)"
              >
                {{ c }}
              </button>
            </div>
          </div>

          <div class="price" v-if="selectedVariant">
            <div class="price__now">{{ format(selectedVariant.price) }}</div>
            <div class="price__old" v-if="selectedVariant.old_price">{{ format(selectedVariant.old_price) }}</div>
          </div>
          <div class="muted small" v-else>Нет доступных вариаций.</div>

          <div class="muted small" v-if="selectedVariant">
            {{ selectedVariant.in_stock ? "В наличии" : "Нет в наличии" }}
          </div>

          <div class="drawer__actions" style="margin-top: 16px;">
            <a
              class="btn"
              :href="buyLink"
              target="_blank"
              rel="noopener"
              :aria-disabled="!selectedVariant || !selectedVariant.in_stock"
              :class="{ 'btn--ghost': !selectedVariant || !selectedVariant.in_stock }"
              @click.prevent="selectedVariant && selectedVariant.in_stock ? openBuyLink() : null"
            >
              {{ selectedVariant && selectedVariant.in_stock ? "Купить в Telegram" : "Нет в наличии" }}
            </a>
            <router-link class="btn btn--ghost" to="/catalog">Каталог</router-link>
          </div>

          <hr class="hr" />

          <div>
            <div class="label">Варианты</div>
            <div class="muted small" v-if="!product.variants.length">Для товара пока нет вариантов.</div>
            <div v-else class="chips">
              <button
                v-for="v in product.variants"
                :key="v.id"
                class="chip"
                :class="{ active: isVariantSelected(v) }"
                @click="selectVariant(v)"
              >
                {{ variantLabel(v) }} · {{ v.in_stock ? "в наличии" : "нет в наличии" }}
              </button>
            </div>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from "vue";
import HeaderBar from "../components/HeaderBar.vue";
import { api, absMedia } from "../api";
import { telegramBuyLink } from "../utils/telegram";
import { useCatalogStore } from "../stores/catalog";
import { useRouter } from "vue-router";

const props = defineProps({
  slug: { type: String, required: true },
});

const MANAGER_USERNAME = import.meta.env.VITE_MANAGER_USERNAME || "vvv_store63";

const product = ref(null);
const loading = ref(true);
const error = ref("");
const menuOpen = ref(false);
const router = useRouter();
const catalogStore = useCatalogStore();

const selectedMemory = ref(null);
const selectedColor = ref("");

const memories = computed(() =>
  product.value?.variants
    ?.map((v) => v.memory_gb)
    .filter((v) => v)
    .filter((v, i, arr) => arr.indexOf(v) === i) || []
);

const colors = computed(() =>
  product.value?.variants
    ?.map((v) => v.color)
    .filter((v) => v)
    .filter((v, i, arr) => arr.indexOf(v) === i) || []
);

const filteredVariants = computed(() => {
  if (!product.value?.variants) return [];
  return product.value.variants.filter((v) => {
    const matchMemory = selectedMemory.value ? v.memory_gb === selectedMemory.value : true;
    const matchColor = selectedColor.value ? v.color === selectedColor.value : true;
    return matchMemory && matchColor;
  });
});

const tags = computed(() =>
  (product.value?.tags || [])
    .map((t) => (typeof t === "string" ? { slug: t, title: t } : { slug: t.slug || t.title, title: t.title || t.slug }))
    .filter((t) => t.slug && t.title)
);

const selectedVariant = computed(() => {
  if (filteredVariants.value.length) return filteredVariants.value[0];
  return product.value?.variants?.[0] || null;
});

const cover = computed(() => absMedia(product.value?.cover));

const productUrl = computed(() => {
  if (!product.value) return window.location.href;
  const origin = typeof window !== "undefined" ? window.location.origin : "";
  return `${origin}/product/${product.value.slug}`;
});

const variantText = computed(() => {
  if (!selectedVariant.value) return "";
  const parts = [];
  if (selectedVariant.value.memory_gb) parts.push(`${selectedVariant.value.memory_gb}GB`);
  if (selectedVariant.value.color) parts.push(selectedVariant.value.color);
  return parts.join(" / ");
});

const buyLink = computed(() =>
  product.value
    ? telegramBuyLink({
        managerUsername: MANAGER_USERNAME,
        productUrl: productUrl.value,
        productTitle: product.value.title,
        variantText: variantText.value,
        price: selectedVariant.value?.price,
      })
    : "#"
);

function format(n) {
  if (!n && n !== 0) return "—";
  return new Intl.NumberFormat("ru-RU").format(n) + " ₽";
}

function variantLabel(v) {
  const parts = [];
  if (v.memory_gb) parts.push(`${v.memory_gb}GB`);
  if (v.color) parts.push(v.color);
  parts.push(format(v.price));
  return parts.join(" · ");
}

async function loadProduct() {
  loading.value = true;
  error.value = "";
  try {
    const res = await api.get(`products/${props.slug}/`);
    product.value = res.data;

    const firstVariant = res.data.variants?.[0];
    selectedMemory.value = firstVariant?.memory_gb || null;
    selectedColor.value = firstVariant?.color || "";
  } catch (e) {
    error.value = "Не удалось загрузить товар";
  } finally {
    loading.value = false;
  }
}

function selectMemory(m) {
  selectedMemory.value = m;
}

function selectColor(c) {
  selectedColor.value = c;
}

function goToTag(slug) {
  catalogStore.tags = [slug];
  catalogStore.page = 1;
  router.push("/catalog");
}

function selectVariant(v) {
  selectedMemory.value = v.memory_gb || null;
  selectedColor.value = v.color || "";
}

function isVariantSelected(v) {
  return (v.memory_gb || null) === selectedMemory.value && (v.color || "") === selectedColor.value;
}

function openBuyLink() {
  window.open(buyLink.value, "_blank", "noopener");
}

onMounted(loadProduct);

watch(
  () => props.slug,
  () => loadProduct()
);
</script>