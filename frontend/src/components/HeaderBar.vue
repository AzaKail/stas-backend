<template>
  <header class="topbar">
    <div class="topbar__left">
      <button class="icon-btn" @click="$emit('openMenu')" aria-label="Открыть меню">☰</button>
      <router-link class="brand" to="/">VVVStore</router-link>
    </div>
    <a class="topbar__cta" href="https://t.me/vvv_store63" target="_blank">Telegram</a>
  </header>
</template>
