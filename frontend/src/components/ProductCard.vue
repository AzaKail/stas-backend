<template>
  <router-link class="card" :to="`/product/${item.slug}`">
    <div class="card__img">
      <img v-if="img" :src="img" :alt="item.title" />
      <div v-else class="ph" />
    </div>
    <div class="card__body">
      <div class="card__title">{{ item.title }}</div>
      <div class="card__sub muted">
        от <b>{{ format(item.min_price) }}</b>
      </div>
      <div class="card__meta muted" v-if="item.warranty">{{ item.warranty }}</div>
      <div class="chips" v-if="tags.length" style="margin-top:8px;">
        <span class="chip muted" v-for="t in tags" :key="t.slug">#{{ t.title }}</span>
      </div>
    </div>
  </router-link>
</template>

<script setup>
import { computed } from "vue";
import { absMedia } from "../api";

const props = defineProps({ item: Object });

const img = computed(() => absMedia(props.item.cover));
const tags = computed(() =>
  (props.item.tags || [])
    .map((t) => (typeof t === "string" ? { slug: t, title: t } : { slug: t.slug || t.title, title: t.title || t.slug }))
    .filter((t) => t.slug && t.title)
);

function format(n) {
  if (!n && n !== 0) return "—";
  return new Intl.NumberFormat("ru-RU").format(n) + " ₽";
}
</script>
