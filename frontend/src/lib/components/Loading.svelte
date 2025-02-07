<script lang="ts">
  export let message: string = 'Loading...'
</script>

<div class="flex items-center justify-center h-full w-full">
  <div class="flex flex-col items-center">
    <div class="animate-spin rounded-full h-16 w-16 border-t-4 border-blue-500"></div>
    <span class="mt-4 text-xl font-semibold">{message}</span>
  </div>
</div>
