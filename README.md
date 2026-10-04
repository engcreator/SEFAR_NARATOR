# SEFAR NARATOR — V1.1 Public Release Candidate

**Stories that bring nature alive.**

SEFAR NARATOR is a guided nature-exploration web experience. Visitors make clear choices, one step at a time, and receive a story that reflects what they are seeking while opening paths to science, questions, activities, and further discovery.

## Public visitor journey

**Audience → Explore → Experience → Language → Create → Story + Discovery**

The profile area is optional and does not determine the audience experience.

## What is ready

- Public landing page and product introduction
- Clear exploration path with numbered steps
- Audience selection for different age contexts and groups
- Nature category and subject selection
- Experience mode and format selection
- Narrative depth selection
- English, French, and Arabic paths
- Continuous Storybook presentation with controlled paragraph width
- Subject-adaptive visual themes
- Nature & Science section with fiction/science distinction
- Questions, observation activities, and related discoveries
- Responsive desktop/mobile-oriented layout
- Local JSON content; no AI dependency

## What is intentionally future work

- AI story enrichment
- AI illustration generation
- Voice/audio generation and playback
- Persistent accounts and database
- Payments/subscriptions
- Native mobile applications
- Custom domain and production analytics

## Run locally

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

## First public deployment

This release is designed for a first public web test using Streamlit Community Cloud or another Streamlit-compatible host.

Before announcing the URL, test the complete journey on desktop and a smartphone-sized viewport:

1. Open the landing page as a new visitor.
2. Start exploring.
3. Make a complete set of choices.
4. Create the experience.
5. Read the continuous story.
6. Check science, questions, activity, and related discoveries.
7. Reset and try a different audience, language, and subject.

## Product principle

**Clear path → clear choices → beautiful interface → meaningful story → further discovery.**
