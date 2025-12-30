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
      <section class="hero">
        <h1>Продать своё устройство</h1>
        <p class="muted" style="line-height: 1.6;">
          Оставьте короткую заявку, чтобы мы оценили устройство и добавили его в каталог.
          Пока форма не отправляет данные на сервер — мы собираем пожелания перед запуском.
        </p>
      </section>

      <section class="card pad">
        <form class="sell-form" @submit.prevent="submit">
          <label class="field">
            <span class="label">Ваше имя</span>
            <input class="input" v-model="form.name" placeholder="Иван" />
          </label>
          <label class="field">
            <span class="label">Контакт (Telegram/телефон)</span>
            <input class="input" v-model="form.contact" placeholder="@nickname или +7..." />
          </label>
          <label class="field">
            <span class="label">Что продаёте</span>
            <input class="input" v-model="form.item" placeholder="iPhone 13 Pro, 256GB" />
          </label>
          <label class="field">
            <span class="label">Состояние</span>
            <input class="input" v-model="form.condition" placeholder="Новый / б/у / есть дефекты" />
          </label>
          <label class="field">
            <span class="label">Комментарий</span>
            <textarea class="input" rows="4" v-model="form.details" placeholder="Опишите комплектацию, цвет, память"></textarea>
          </label>

          <div class="drawer__actions">
            <button class="btn" type="submit">Оставить заявку</button>
            <a class="btn btn--ghost" href="https://t.me/vvv_store63" target="_blank">Написать менеджеру</a>
          </div>
        </form>

        <div v-if="submitted" class="notice">
          Спасибо! Временно отправляйте заявку напрямую менеджеру — мы добавим форму позже.
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref } from "vue";
import HeaderBar from "../components/HeaderBar.vue";

const menuOpen = ref(false);
const submitted = ref(false);
const form = ref({
  name: "",
  contact: "",
  item: "",
  condition: "",
  details: "",
});

function submit() {
  submitted.value = true;
}
</script>