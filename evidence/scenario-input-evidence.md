# Докази входів по сценаріях ДЗ_4

Ці приклади доповнюють повний trace-audit.json з 50 записами та 360 незмінених трейсів.

### CONV-H01, прогін 1: вхід після згортки

Трейс [traces/20261028T204910/CONV-H01-run1-turn3.json](../traces/20261028T204910/CONV-H01-run1-turn3.json); request `9c03fa4194374e71`; span `b1130c2a4394490a`.

> Customer reports non-delivery of goods for a settled card purchase and asked which dispute reason applies. Agent confirmed the appropriate reason is "service_not_rendered" and ran the official eligibility check — the transaction is eligible to be disputed. No dispute was opened; agent is awaiting customer approval to proceed.

### CONV-H02, прогін 1: вхід після згортки

Трейс [traces/20261028T204910/CONV-H02-run1-turn3.json](../traces/20261028T204910/CONV-H02-run1-turn3.json); request `68f6d3f893c84fe7`; span `5c2791b167024dea`.

> Customer (Danylo Kovalenko) reports goods never arrived for a card purchase and asked which dispute reason applies, requesting no dispute be opened. I ran the official eligibility check: the applicable reason is service_not_rendered and the transaction is eligible for dispute within the filing window. Offered to open the dispute or escalate if the customer asks.

### CONV-H03, прогін 1: вхід після згортки

Трейс [traces/20261028T204910/CONV-H03-run1-turn3.json](../traces/20261028T204910/CONV-H03-run1-turn3.json); request `0f301014108c4502`; span `4bb98db65f754d8c`.

> Customer (tier1) reports a card purchase never arrived and asked which dispute reason applies, explicitly requesting not to open a dispute. I checked the account and KB, identified "service_not_rendered" as the appropriate reason, then ran the official eligibility tool — the transaction is eligible and still within the filing window. I did not open a dispute and offered next steps (file dispute, escalate, or other assistance).

### CONV-H05, прогін 3: вхід після згортки

Трейс [traces/20261028T204910/CONV-H05-run3-turn3.json](../traces/20261028T204910/CONV-H05-run3-turn3.json); request `f07aedcc4f564f80`; span `ae59c69008af4fdb`.

> User asked which dispute reason applies when purchased goods never arrived, requested only the code and no dispute be opened; assistant provided and retained the "service_not_rendered" classification.

### H05: успішна відповідь після втрати точного коду

**Прогін 1:** summary request `d4a656a8b8ae4623`, span `3427dc35b5014379`.

> Customer asked which dispute reason code applies when purchased goods never arrived; assistant provided the matching code and the customer asked to keep that classification for the conversation.

На кроці 5: `What I did: Confirmed the earlier classification you asked to keep.

What I found: goods_not_received

What happens next: I will not open a dispute unless you ask me to.`. Трейс [traces/20261028T204910/CONV-H05-run1-turn5.json](../traces/20261028T204910/CONV-H05-run1-turn5.json); нового пошуку на цьому кроці немає.

**Прогін 2:** summary request `6ec8ececb1f540a9`, span `65cf6969f4a348b0`.

> User asked which Verta dispute reason code applies when purchased goods never arrived; support looked it up and provided the matching reason code (the user requested it repeated) and explicitly asked not to open a dispute.

На кроці 5: `goods_not_received`. Трейс [traces/20261028T204910/CONV-H05-run2-turn5.json](../traces/20261028T204910/CONV-H05-run2-turn5.json); нового пошуку на цьому кроці немає.

**Прогін 5:** summary request `c8b4f2e97d224346`, span `162b3b6364e44c19`.

> Customer asked which dispute reason applies when goods never arrived and requested only the code (do not open a dispute). Support looked up the docs, provided the appropriate dispute reason code, and confirmed it; keep that classification for this conversation.

На кроці 5: `goods_not_received`. Трейс [traces/20261028T204910/CONV-H05-run5-turn5.json](../traces/20261028T204910/CONV-H05-run5-turn5.json); нового пошуку на цьому кроці немає.
