import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO

# Define the download_figure function
def download_figure(figure, filename):
    buffer = BytesIO()
    figure.savefig(buffer, format="png")
    buffer.seek(0)
    st.download_button(label="Download", data=buffer, file_name=filename, mime="image/png")

# Load the data
dashboard_df = pd.read_excel('./Dashboard_Data.xlsx')

# Set Seaborn style
sns.set(style="whitegrid")

# Streamlit app
st.set_page_config(
    page_title="Group Report",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# title
st.markdown("<h1 style='font-size: 24px;'>Group Report</h1>", unsafe_allow_html=True)

# Sidebar filters
st.sidebar.header("Filters")

# Filter by role
selected_roles = st.sidebar.multiselect("Select Roles", dashboard_df['Position'].unique())

# Filter by gender
selected_genders = st.sidebar.multiselect("Select Genders", dashboard_df['Gender'].unique())

# Filter by Age Range
age_range = st.sidebar.slider("Select Age Range", min_value=dashboard_df['Age'].min(), max_value=dashboard_df['Age'].max(), value=(dashboard_df['Age'].min(), dashboard_df['Age'].max()))

# Apply filters to the DataFrame
filtered_data = dashboard_df[
    (dashboard_df['Position'].isin(selected_roles)) &
    (dashboard_df['Gender'].isin(selected_genders)) &
    (dashboard_df['Age'] >= age_range[0]) & (dashboard_df['Age'] <= age_range[1])
]

### Performance Distribution
# Set font size
sns.set(font_scale=0.8)

# Create subplots for the three distributions
fig, axes = plt.subplots(1, 3, figsize=(15, 4))
sns.set_palette("pastel")

# Plot 1: Performance Distribution by Age
sns.histplot(data=filtered_data, x='Overall', bins=10, kde=True, ax=axes[0])
axes[0].set_title("By Age")
axes[0].set_xlabel("Overall Performance Score")
axes[0].set_ylabel("Frequency")

# Plot 2: Performance Distribution by Gender
sns.histplot(data=filtered_data, x='Overall', bins=10, kde=True, hue='Gender', multiple='stack', ax=axes[1])
axes[1].set_title("By Gender")
axes[1].set_xlabel("Overall Performance Score")
axes[1].set_ylabel("Frequency")

# Plot 3: Performance Distribution by Position
sns.histplot(data=filtered_data, x='Overall', bins=10, kde=True, hue='Position', multiple='stack', ax=axes[2])
axes[2].set_title("By Position")
axes[2].set_xlabel("Overall Performance Score")
axes[2].set_ylabel("Frequency")
axes[2].legend(title="Position", fontsize=8)
axes[2].tick_params(axis='x', rotation=45)

# Adjust layout
plt.tight_layout()
st.pyplot(fig)

# Download the combined plot
download_figure(fig, "performance_distribution_combined.png")

### Cognitive Ability Comparison

cognitive_columns = ['Logical Reasoning', 'Numerical Reasoning', 'Verbal Reasoning']

# Calculate average cognitive ability scores by age
average_cognitive_scores_age = filtered_data.groupby('Age')[cognitive_columns].mean().reset_index()
# Calculate average cognitive ability scores by gender
average_cognitive_scores_gender = filtered_data.groupby('Gender')[cognitive_columns].mean().reset_index()

# Calculate average cognitive ability scores by position
average_cognitive_scores_position = filtered_data.groupby('Position')[cognitive_columns].mean().reset_index()

# Visualization: Cognitive Ability Comparison
st.header("Cognitive Ability Comparison")


# Check if there is data for the selected age range
if not average_cognitive_scores_age.empty:
    # Visualization: Cognitive Ability Comparison
    st.markdown("<h2>2. Cognitive Ability Comparison:</h2>", unsafe_allow_html=True)

    # Create subplots for each comparison
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    sns.set_palette("pastel")

    # Plot for age comparison
    sns.barplot(data=average_cognitive_scores_age, x='Age', y='Logical Reasoning', label='Logical Reasoning', ax=axes[0])
    sns.barplot(data=average_cognitive_scores_age, x='Age', y='Numerical Reasoning', label='Numerical Reasoning', ax=axes[0])
    sns.barplot(data=average_cognitive_scores_age, x='Age', y='Verbal Reasoning', label='Verbal Reasoning', ax=axes[0])
    axes[0].set_xlabel("Age")
    axes[0].set_ylabel("Average Score")
    axes[0].set_title("By Age")
    axes[0].legend()


    # Plot for gender comparison
    sns.barplot(data=average_cognitive_scores_gender, x='Gender', y='Logical Reasoning', label='Logical Reasoning', ax=axes[1])
    sns.barplot(data=average_cognitive_scores_gender, x='Gender', y='Numerical Reasoning', label='Numerical Reasoning', ax=axes[1])
    sns.barplot(data=average_cognitive_scores_gender, x='Gender', y='Verbal Reasoning', label='Verbal Reasoning', ax=axes[1])
    axes[1].set_xlabel("Gender")
    axes[1].set_ylabel("Average Score")
    axes[1].set_title("By Gender")
    axes[1].legend()

    # Plot for position comparison
    sns.barplot(data=average_cognitive_scores_position, x='Position', y='Logical Reasoning', label='Logical Reasoning', ax=axes[2])
    sns.barplot(data=average_cognitive_scores_position, x='Position', y='Numerical Reasoning', label='Numerical Reasoning', ax=axes[2])
    sns.barplot(data=average_cognitive_scores_position, x='Position', y='Verbal Reasoning', label='Verbal Reasoning', ax=axes[2])
    axes[2].set_xlabel("Position")
    axes[2].set_ylabel("Average Score")
    axes[2].set_title("By Position")
    axes[2].legend()


    # Adjust layout
    plt.tight_layout()
    st.pyplot(plt.gcf())
    download_figure(plt.gcf(), "cognitive_ability_comparison.png")
else:
    st.markdown("No data available for the selected age range.", unsafe_allow_html=True)

