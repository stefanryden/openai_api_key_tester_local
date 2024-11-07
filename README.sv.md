# OpenAI API-nyckel Testare

Ett omfattande Python-verktyg för att testa och validera OpenAI API-nycklar, med både GUI och CLI-gränssnitt.

## Funktioner

- Modernt grafiskt användargränssnitt (GUI) med intuitiva kontroller
- Kommandoradsgränssnitt (CLI) för automatisering
- Validerar API-nyckelns format
- Testar API-nyckelns funktionalitet med OpenAI:s API
- Stöd för att testa flera OpenAI-modeller:
  - GPT-4 och varianter (gpt-4, gpt-4-turbo-preview, gpt-4-1106-preview)
  - GPT-4 Vision Preview
  - GPT-3.5 Turbo och varianter (gpt-3.5-turbo, gpt-3.5-turbo-16k, gpt-3.5-turbo-1106)
  - DALL-E 3
  - Text Embeddings (text-embedding-ada-002)
- Ger tydlig återkoppling om API-nyckelns status och modelltillgänglighet
- Visar användningsstatistik och faktureringsinformation:
  - API-status
  - Kvottillgänglighet
  - Tidsstämpel för senaste kontrollen
- Minimal tokenanvändning vid testning
- Säker nyckelhantering med visa/dölj-funktionalitet
- Förloppsindikator för modelltestning
- Omfattande felhantering

## Krav

- Python 3.7 eller högre
- OpenAI Python-paket

## Installation

Du kan installera paketet med pip:

```bash
pip install openai-api-key-tester
```

Eller klona detta repository och installera från källkod:

1. Klona detta repository eller ladda ner filerna
2. Installera det nödvändiga paketet:

```bash
pip install .
```

## Användning

### GUI-läge

1. Starta GUI:t:
```bash
api-key-tester-gui
```

2. Ange din OpenAI API-nyckel i det säkra inmatningsfältet
3. Välj modeller att testa i modellvalslistan
4. Klicka på "Test API Key" för att starta testprocessen
5. Visa resultat i det scrollbara resultatområdet

### CLI-läge

1. Sätt din OpenAI API-nyckel som en miljövariabel:
```bash
export OPENAI_API_KEY='din-api-nyckel-här'
```

2. Kör CLI-verktyget:
```bash
api-key-tester
```

Skriptet kommer att:
- Visa användningsstatistik och kvotinformation
- Validera nyckelformatet
- Testa åtkomst till alla tillgängliga modeller
- Visa resultat för varje testad modell

## Tillgängliga Modeller

- GPT-4 (gpt-4)
- GPT-4 Turbo Preview (gpt-4-turbo-preview)
- GPT-4 1106 Preview (gpt-4-1106-preview)
- GPT-4 Vision Preview (gpt-4-vision-preview)
- GPT-3.5 Turbo (gpt-3.5-turbo)
- GPT-3.5 Turbo 16k (gpt-3.5-turbo-16k)
- GPT-3.5 Turbo 1106 (gpt-3.5-turbo-1106)
- DALL-E 3 (dall-e-3)
- Text Embedding Ada 002 (text-embedding-ada-002)

## Felmeddelanden

Verktyget ger olika felmeddelanden beroende på problemet:
- Ogiltigt nyckelformat
- Ogiltig API-nyckel
- Modellspecifika åtkomstfel
- Anslutningsfel
- Kvotöverskridningsfel
- Andra API-relaterade fel

## Säkerhetsanmärkningar

- API-nycklar lagras aldrig permanent
- GUI:t erbjuder ett säkert inmatningsfält med visa/dölj-funktionalitet
- Nycklar rensas från minnet efter testning
- Användning av miljövariabler i CLI-läge för säker nyckelhantering

## Observera

Detta verktyg använder minimal tokenanvändning för testning för att undvika onödig API-användning. Varje modelltest använder endast 1 token för att verifiera tillgänglighet, förutom för DALL-E 3 och Vision-modeller som kräver specifika testinmatningar.
