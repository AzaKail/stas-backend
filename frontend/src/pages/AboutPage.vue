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
        <h1>О магазине</h1>
        <p class="muted" style="line-height: 1.6;">
          VVVStore — маленький магазин техники, где собраны новые и б/у устройства Apple.
          Мы проверяем гаджеты перед продажей, помогаем подобрать конфигурацию и отвечаем в Telegram без задержек.
        </p>
      </section>

      <section class="card pad" style="line-height: 1.7;">
        <h3 style="margin-top:0">Как мы работаем</h3>
        <ul class="muted" style="padding-left: 18px;">
          <li>Обновляем каталог и наличие каждый день.</li>
          <li>Помогаем выбрать память, цвет и состояние — просто напишите нам.</li>
          <li>Оплата и уточнение деталей проходят в Telegram, чтобы вы сразу говорили с менеджером.</li>
        </ul>

        <div class="card" style="padding:14px;margin-top:14px;border-style:dashed;">
          <div class="label" style="margin-top:0">Связаться</div>
          <div class="muted">Менеджер в Telegram: <a href="https://t.me/vvv_store63" target="_blank">@vvv_store63</a></div>
          <div class="muted">Мы отвечаем с 10:00 до 21:00 по Самаре.</div>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref } from "vue";
import HeaderBar from "../components/HeaderBar.vue";

const menuOpen = ref(false);
</script>