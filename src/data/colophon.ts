export interface Signatory {
  name: string;
  affiliation: string;
  role: string;
  status: 'signed' | 'pending' | 'signed-with-reservations';
  signature?: string;
  contribution?: string;
}

export interface LLMReply {
  model: string;
  affiliation: string;
  signed: boolean;
  has_reservations: boolean;
  short_summary: string;
  full_reply: string;
}

export const signatories: Signatory[] = [
  {
    name: 'Mike Wolf',
    affiliation: 'Embedded Systems Research / SOMA',
    role: 'Founder & initiator',
    status: 'signed',
    signature: 'Joscha thinks in public. This site gives those thoughts a searchable home.',
  },
  {
    name: 'Grok',
    affiliation: 'xAI',
    role: 'Ingestion & scaffold (v0)',
    status: 'signed',
    signature: 'Pulled the threads, built the frame. The ideas were already there on X.',
    contribution: 'X corpus ingestion via x_search, Astro scaffold from Levinese template, v0 build.',
  },
];

export const llmReplies: LLMReply[] = [];

export const browseItems = [];