<script lang="ts" setup>
definePage({
  name: 'Login',
});

const { user, login } = useAuth();
</script>

<template>
  <div wh-screen f-cer bg-page>
    <ab-container :title="$t('login.title')" w-365 max-w="90%">
      <div space-y-16>
        <ab-label :label="$t('login.username')">
          <input
            v-model="user.username"
            type="text"
            placeholder="username"
            ab-input
          />
        </ab-label>

        <ab-label :label="$t('login.password')">
          <input
            v-model="user.password"
            type="password"
            placeholder="password"
            ab-input
            @keyup.enter="login"
          />
        </ab-label>

        <div line></div>

        <div flex="~ justify-end">
          <ab-button size="small" @click="login">
            {{ $t('login.login_btn') }}
          </ab-button>
        </div>
      </div>
    </ab-container>
  </div>
</template>
