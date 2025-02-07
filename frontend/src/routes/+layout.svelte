<script lang="ts">
  import '../app.css'
  import 'leaflet/dist/leaflet.css'
  import Header from '$components/Header.svelte'
  import Footer from '$components/Footer.svelte'
  let { children } = $props()
</script>

<div class="flex flex-col min-h-screen">
  <Header />

  <!-- flex-grow autofill space left -->
  <main class="flex-grow">
    {@render children()}
  </main>

  <Footer />
</div>
