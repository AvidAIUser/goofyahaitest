# CoolBlock AI – Build Timeline (June 14-21)

## Phase 1: Foundation Setup (June 14-15)

### June 14 – Kickoff & Project Setup
**Tasks**:
- [ ] Watch hackathon kickoff livestream (10:00 AM ET)
- [ ] Set up GitHub repo for the project
- [ ] Create Streamlit project structure
- [ ] Set up Google Colab notebook for model training
- [ ] Divide team roles:
  - **Lead Developer**: AI model, backend
  - **Data Researcher**: Data collection, OpenStreetMap/weather API integration
  - **UI/Presenter**: Streamlit frontend, video production

**Deliverable**: Basic Streamlit app with map display (can be placeholder initially)

### June 15 – Data Collection Begins
**Tasks**:
- [ ] Set up image collection pipeline (Google Street View static API)
- [ ] Install LabelImg for image labeling
- [ ] Start collecting ~100 street view images from heat-vulnerable areas
- [ ] Begin labeling images as "shade" or "no-shade"
- [ ] Research OpenStreetMap data structure for cooling centers

**Deliverable**: 100+ labeled images, OpenStreetMap cooling center dataset

---

## Phase 2: AI Model Development (June 16-17)

### June 16 – Model Training
**Tasks**:
- [ ] Collect remaining 400 street view images (~500 total)
- [ ] Label all images using LabelImg
- [ ] Generate 200 synthetic augmented images (rotation, brightness)
- [ ] Set up TensorFlow/Keras CNN model in Google Colab
- [ ] Split data: 70% training, 15% validation, 15% test
- [ ] Train model (run in Google Colab for 2-4 hours)

**Deliverable**: Trained CNN model saved as `.h5` file

### June 17 – Model Integration & API Setup
**Tasks**:
- [ ] Download trained model from Colab
- [ ] Integrate model into Streamlit app (load `.h5` file)
- [ ] Add image upload feature to Streamlit UI
- [ ] Test model predictions on new images
- [ ] Integrate OpenStreetMap API to fetch cooling center locations
- [ ] Integrate Open-Meteo weather API for real-time temperature

**Deliverable**: Streamlit app with working model predictions + API data

---

## Phase 3: Core Logic & Risk Scoring (June 18)

### June 18 – Risk Algorithm & Map Display
**Tasks**:
- [ ] Build risk scoring formula:
  - Base risk = 0 (safe)
  - If temperature > 95°F → risk += 30
  - If shade score < 40% → risk += 40
  - If shade score 40-60% → risk += 20
  - If no nearby cooling center → risk += 10
  - Final risk: 0-100 (map as green/yellow/red)
- [ ] Create color-coded map (green < 40, yellow 40-70, red > 70)
- [ ] Add cooling center locations as pins on map
- [ ] Add walking distance calculation to nearest 3 cooling centers
- [ ] Test on different addresses and ZIP codes

**Deliverable**: Functional map with risk scores and cooling center directions

---

## Phase 4: UI Polish & Responsible AI (June 19)

### June 19 – Frontend Polish & Guardrails
**Tasks**:
- [ ] Add confidence threshold UI (show "unsure" if shade score 40-60%)
- [ ] Add link to satellite view for manual verification
- [ ] Always display emergency numbers (911, poison control) on map
- [ ] Add "Report cooling center closed" feature (user override)
- [ ] Add instructions and help text
- [ ] Test on mobile phone (responsive design)
- [ ] Add error handling for API failures
- [ ] Performance optimization (cache results for 1 hour)

**Deliverable**: Polished UI with responsible AI safeguards

---

## Phase 5: Documentation & Testing (June 20)

### June 20 – Video & README
**Tasks**:
- [ ] Write comprehensive GitHub README (setup, usage, model info)
- [ ] Create `.env.example` file (API keys template)
- [ ] Record pitch video (3-5 minutes):
  - Hook (problem statement)
  - Solution (how app works)
  - Demo (live walkthrough)
  - Impact (user testimonial or use case)
  - Responsible AI (safeguards)
- [ ] Edit and upload video (YouTube unlisted or Loom)
- [ ] Full end-to-end testing on a fresh device
- [ ] Prepare all Devpost submission text

**Deliverable**: Video + README + submission text ready

---

## Phase 6: Submission Prep (June 21)

### June 21 – Final Checks & Submit
**Tasks**:
- [ ] **Morning**: Final bug fixes and testing
- [ ] **Afternoon**: 
  - [ ] Gather all team members for final review
  - [ ] Double-check all submission fields
  - [ ] Verify qualifier approval code
  - [ ] Confirm all team member emails and names
  - [ ] Test demo link one final time
  - [ ] Verify video link works
- [ ] **6:00 PM ET**: Start Devpost submission process
- [ ] **Before 11:59 PM ET**: Submit on Devpost

**DO NOT WAIT UNTIL 11:58 PM – Submit by 11:00 PM to be safe**

**Deliverable**: Completed Devpost submission with all components

---

## Key Milestones & Checkpoints

| Date | Checkpoint | Status |
|------|-----------|--------|
| June 14 | Kickoff + basic Streamlit setup | ⬜ |
| June 15 | 100+ labeled images collected | ⬜ |
| June 16 | Model trained and tested | ⬜ |
| June 17 | Model integrated + APIs working | ⬜ |
| June 18 | Risk scoring + color-coded map | ⬜ |
| June 19 | UI polished + safeguards added | ⬜ |
| June 20 | Video + README complete | ⬜ |
| June 21 | **SUBMITTED** ✅ | ⬜ |

---

## Risk Management

### What Could Go Wrong?

| Risk | Mitigation |
|------|-----------|
| Not enough training images | Use synthetic data augmentation (200 extra images from rotations/brightness) |
| Model accuracy too low | Retrain with different hyperparameters; simplify to binary (shade/no-shade) |
| API rate limits exceeded | Implement caching (1-hour TTL), use free tier limits carefully |
| Map too slow on mobile | Simplify GeoJSON, cluster markers, lazy-load cooling centers |
| Video upload fails | Record locally, have backup Loom account ready |
| Model file too large | Use model compression (TensorFlow Lite) if needed |
| Qualifier code issue | Request resend from hackathon.qualifier@usaii.org ASAP |

---

## Team Communication

**Daily standups** (async on Discord):
- 📌 **#coolblock-ai**: What did you do? What are you doing today? Any blockers?

**Shared resources**:
- GitHub repo: Central code
- Google Drive: Shared datasets, scripts
- Discord: Daily updates + troubleshooting

**Backup plan**: If one person gets sick, other roles can pick up their tasks.
