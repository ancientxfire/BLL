<template>
  <Suspense>
    <UApp>
      <UHeader>
        <template #left>
          <RouterLink to="/" class=" space-x-2">
            <UButton to="/sma">SM</UButton>
            <UButton to="/v1">V1</UButton>
          </RouterLink>

          <TemplateMenu />
        </template>

        <template #right>
          <UColorModeButton />

          <UButton
            to="https://github.com/ancientxfire/bll"
            target="_blank"
            icon="simple-icons:github"
            aria-label="GitHub"
            color="neutral"
            variant="ghost"
          />
        </template>
      </UHeader>

      <UMain>
        <RouterView />
      </UMain>

      

    </UApp>
  </Suspense>
</template>
