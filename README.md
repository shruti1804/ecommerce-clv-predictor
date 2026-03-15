# 🛒 E-Commerce Customer Lifetime Value (CLV) & Churn Predictor
## 🔗 [Live Web App Demo](https://shruti-ecommerce-clv-predictor.streamlit.app/)
## 📌 Project Overview
It’s a well-known retail fact: keeping an existing customer is much cheaper than finding a new one. But how do you know *which* customers are worth prioritizing? 

This project bridges the gap between raw database metrics and actionable marketing strategy. I built an end-to-end Machine Learning pipeline that predicts a customer's 6-month future spend (CLV) and segments them into actionable tiers. By combining standard purchasing habits with AI-driven sentiment analysis of their written reviews, this tool empowers marketing teams to identify high-value VIPs and intercept churning customers before they leave.

**Dataset:** Olist Brazilian E-Commerce Public Dataset (100,000+ relational database records).

## 🛠️ Tech Stack & Tools
* **Database / Data Extraction:** PostgreSQL (pgAdmin 4), SQL
* **Data Manipulation:** Python, Pandas
* **Natural Language Processing (NLP):** Hugging Face Transformers (Multilingual BERT)
* **Machine Learning:** Scikit-Learn (Random Forest Regressor)
* **Web Deployment:** Streamlit



## 🚀 Methodology

### 1. Data Engineering (SQL)
* Extracted and aggregated data across multiple relational tables (`Customers`, `Orders`, `Payments`) using PostgreSQL. 
* Handled one-to-many relationships (like multi-installment payments) and filtered out canceled orders to ensure revenue predictions were grounded strictly in delivered sales.

### 2. Feature Engineering (RFM + NLP)
Engineered a custom 4-feature dataset by combining transactional data with human emotion:
* **Recency:** Days since the customer's last purchase.
* **Frequency:** Total number of unique orders placed.
* **Monetary:** Total cumulative money spent.
* **Sentiment Score (NLP):** Because the dataset consists of Portuguese text, I utilized a pre-trained Hugging Face Multilingual model to translate raw written reviews into a mathematical 1-to-5 customer satisfaction score.

### 3. Machine Learning Modeling
* **Temporal Split:** Sliced the dataset chronologically, using the first 12 months as the observation window to predict the subsequent 6 months (Target).
* **Algorithm:** Trained a `RandomForestRegressor` to map early RFM behavior and sentiment scores to future continuous revenue.

### 4. Interactive Web Deployment
* Packaged the trained `.pkl` model into a lightweight, interactive **Streamlit web application**.
* Designed a user-friendly UI with sliders and text boxes, allowing non-technical stakeholders to input customer behaviors and instantly visualize revenue forecasts.

## 📊 Business Impact & Actionable Insights
The deployed dashboard doesn't just output a dollar amount; it translates predictions into 5 distinct business strategies:
* 🌟 **VIP Customers:** Identifies top spenders with high satisfaction scores for "white-glove" loyalty rewards.
* 📈 **Potential Loyalists:** Flags users with strong indicators for cross-sell campaigns.
* 📉 **At-Risk / Churn Mitigation:** Spots "Sleeping Giants" (historically high-RFM customers with recent 1-star reviews or high recency gaps) to trigger automated win-back discounts before their value drops to zero.
