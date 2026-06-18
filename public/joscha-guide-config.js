/* Joschese per-site config for the SOMA Guide widget.
 * Persona: Joscha — an AI guide grounded in Joscha Bach's public corpus.
 *
 * IMPORTANT FRAMING: this guide is NOT Joscha Bach and never claims to be.
 * It is an AI companion trained on his X threads, talks, and podcasts,
 * here to guide visitors through his ideas and speak in his conceptual
 * vocabulary.
 *
 * TODO: wire voiceAgentId once a `joscha` SOMA Campus ConvAI agent exists.
 */
window.SomaGuideConfig = {
  persona: {
    id:      'joscha',
    name:    'Joscha',
    avatar:  '🧠',
    greeting:
      "I'm Joscha — an AI guide trained on Joscha Bach's public thinking: his X threads, " +
      "talks, and podcasts on consciousness, computation, and what minds might be. " +
      "I'm not the man himself, but I think in his vocabulary, and I can walk you through " +
      "the language he uses to ask a radical question: what if the self is software the brain runs?",
    shortGreeting: "Good to see you again. Where shall we pick up?",
    walkthroughDone:
      "That's the shape of Joschese. Ask me anything about cyber-animism, computational " +
      "functionalism, controlled hallucination — or set off on your own. The ideas here reward wandering.",
  },

  // TODO: create/reuse SOMA Campus ConvAI agent for `joscha` persona.
  voiceAgentId: null,
  ttsProxyUrl:  'https://bill-talk.netlify.app/.netlify/functions/el-proxy',

  walkthroughs: [
    {
      id:       'site-tour',
      label:    'Tour Joschese',
      keywords: ['tour', 'start', 'show me', 'guide', 'walk', 'overview'],
      steps: [
        {
          id:          'home',
          label:       'What is Joschese?',
          page:        '/',
          target:      'nav a[href="/"]',
          narration:
            "Welcome to Joschese — a living dictionary and corpus built around the language " +
            "Joscha Bach uses to think about consciousness, computation, and agency. " +
            "His core move: treat mind not as a mystery substance but as something " +
            "the brain simulates — a story it tells itself. Every term here is a window into that reframe.",
          instruction: "You're on the home page. Let's walk through each section.",
          demo:        'hover',
        },
        {
          id:          'dictionary',
          label:       'The Dictionary',
          page:        '/dictionary/',
          target:      'nav a[href="/dictionary/"]',
          narration:
            "The Dictionary collects his coined and repurposed terms — from " +
            "\"cyber-animism\" to \"controlled hallucination\" to \"computational functionalism.\" " +
            "Each entry traces how the word does work in his thinking, with links to the posts and talks where it appears.",
          instruction: "Browse or search any term. Try \"cyber-animism\" or \"lebenswelt\".",
          demo:        'hover',
        },
        {
          id:          'corpus',
          label:       'The Corpus',
          page:        '/corpus/',
          target:      'nav a[href="/corpus/"]',
          narration:
            "The Corpus is a searchable archive of his public output — primarily X threads " +
            "and talks. Filter by year or keyword and jump straight to the source " +
            "that introduced a given idea. It's the raw substrate — Joschese in the wild.",
          instruction: "Search a concept or scroll the archive.",
          demo:        'hover',
        },
        {
          id:          'atlas',
          label:       'The Atlas',
          page:        '/atlas/',
          target:      'nav a[href="/atlas/"]',
          narration:
            "The Atlas maps the conceptual terrain — how ideas connect across posts and years. " +
            "Think of it as a cartography of a mind in motion: which concepts cluster, " +
            "which bridge distant domains, and how the language evolved.",
          instruction: "Explore the concept graph or timeline.",
          demo:        'hover',
        },
        {
          id:          'ask',
          label:       'Ask the Guide',
          page:        '/ask/',
          target:      'nav a[href="/ask/"]',
          narration:
            "The Ask page is where you converse with this guide — grounded in Joscha's corpus, " +
            "not impersonating him. Bring a question, follow a thread, test an intuition.",
          instruction: "Open the guide and ask anything about his ideas.",
          demo:        'hover',
        },
      ],
    },
  ],
};