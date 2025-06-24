import pandas as pd
from datetime import datetime, timedelta
import re
import sys

def load_data(filepath):
    try:
        df = pd.read_csv(filepath)
        return df
    except FileNotFoundError:
        print(f"Error: {filepath} not found. Please upload the file.")
        sys.exit(1)
    except Exception as e:
        print(f"Error loading data: {e}")
        sys.exit(1)

def extract_dummy_price_product(text):
    price_match = re.search(r'(\d+)\s*(ብር|ETB)', str(text))
    product_match = re.search(r'(\w+)\s*(ሽያጭ|አለ)', str(text))
    price = price_match.group(1) if price_match else None
    product = product_match.group(1) if product_match else None
    return price, product

def extract_entities(df):
    # Replace this with your real NER model integration
    try:
        df[['predicted_price', 'predicted_product']] = df['post_text'].apply(
            lambda x: pd.Series(extract_dummy_price_product(x))
        )
        return df
    except Exception as e:
        print(f"Error extracting entities: {e}")
        sys.exit(1)

def prepare_data(df):
    try:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['predicted_price'] = pd.to_numeric(df['predicted_price'], errors='coerce')
        return df
    except Exception as e:
        print(f"Error preparing data: {e}")
        sys.exit(1)

def calculate_vendor_metrics(df):
    vendor_metrics = {}
    for vendor_name, vendor_df in df.groupby('vendor_name'):
        metrics = {}
        # Posting Frequency
        if not vendor_df.empty:
            time_range = vendor_df['timestamp'].max() - vendor_df['timestamp'].min()
            total_posts = len(vendor_df)
            time_range_weeks = time_range.total_seconds() / (7 * 24 * 3600) + 1e-9
            posting_frequency = total_posts / time_range_weeks
            metrics['Posts/Week'] = posting_frequency
        else:
            metrics['Posts/Week'] = 0
        # Average Views per Post
        metrics['Avg. Views/Post'] = vendor_df['views'].mean() if not vendor_df.empty else 0
        # Top Performing Post
        if not vendor_df.empty and 'views' in vendor_df.columns:
            top_post = vendor_df.loc[vendor_df['views'].idxmax()]
            metrics['Top Post Text'] = top_post['post_text']
            metrics['Top Post Product'] = top_post.get('predicted_product', 'N/A')
            # Round top post price to 2 decimals if possible
            try:
                top_post_price = float(top_post.get('predicted_price', 'N/A'))
                metrics['Top Post Price'] = round(top_post_price, 2)
            except (ValueError, TypeError):
                metrics['Top Post Price'] = top_post.get('predicted_price', 'N/A')
        else:
            metrics['Top Post Text'] = 'N/A'
            metrics['Top Post Product'] = 'N/A'
            metrics['Top Post Price'] = 'N/A'
        # Average Price Point
        valid_prices = vendor_df['predicted_price'].dropna()
        if not valid_prices.empty:
            metrics['Avg. Price (ETB)'] = round(valid_prices.mean(), 2)
        else:
            metrics['Avg. Price (ETB)'] = 0
        vendor_metrics[vendor_name] = metrics
    return vendor_metrics

def calculate_lending_score(avg_views, posting_frequency, avg_price):
    # Example formula - adjust weights as needed
    score = (avg_views * 0.5) + (posting_frequency * 0.5) + (avg_price * 0.01)
    return score

def create_scorecard(vendor_metrics):
    for vendor_name, metrics in vendor_metrics.items():
        avg_views = metrics.get('Avg. Views/Post', 0)
        posting_frequency = metrics.get('Posts/Week', 0)
        avg_price = metrics.get('Avg. Price (ETB)', 0)
        metrics['Lending Score'] = calculate_lending_score(avg_views, posting_frequency, avg_price)
    vendor_scorecard_df = pd.DataFrame.from_dict(vendor_metrics, orient='index')
    report_columns = [
        'Avg. Views/Post', 'Posts/Week', 'Avg. Price (ETB)', 'Lending Score',
        'Top Post Text', 'Top Post Product', 'Top Post Price'
    ]
    vendor_scorecard_df = vendor_scorecard_df[report_columns]
    vendor_scorecard_df = vendor_scorecard_df.sort_values(by='Lending Score', ascending=False)
    return vendor_scorecard_df

def main():
    filepath = '/content/amharic_ecommerce_data.csv'  # Change as needed
    df = load_data(filepath)
    df = extract_entities(df)
    df = prepare_data(df)
    vendor_metrics = calculate_vendor_metrics(df)
    scorecard = create_scorecard(vendor_metrics)
    print("## Vendor Scorecard")
    print(scorecard)
    # Optionally, print top post details for each vendor
    print("\n## Top Performing Posts per Vendor")
    for vendor_name, metrics in vendor_metrics.items():
        print(f"\nVendor: {vendor_name}")
        print(f"  Top Post Text: {metrics['Top Post Text']}")
        print(f"  Top Post Product: {metrics['Top Post Product']}")
        print(f"  Top Post Price: {metrics['Top Post Price']}")

if __name__ == '__main__':
    main()