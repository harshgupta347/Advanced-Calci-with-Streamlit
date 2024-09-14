# !pip install streamlit numpy matplotlib pandas 
# .\myenv\Scripts\Activate
# streamlit run filename.py

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Function for non-pie charts
def parse_plot_data(data_input):
    data = {}
    try:
        for item in data_input.split(';'):
            key, values = item.split(':')
            key = key.strip()
            values = [value.strip() for value in values.split(',')]
            if key in ['x', 'y']:
                data[key] = values  # Keep as strings for x-axis categories
    except Exception as e:
        st.error(f"Error parsing data: {e}")
    return data

# Function for pie charts
def parse_pie_data(data_input):
    data = {}
    try:
        for item in data_input.split(';'):
            key, values = item.split(':')
            key = key.strip()
            values = [value.strip() for value in values.split(',')]
            if key == 'labels':
                data[key] = values
            elif key == 'sizes':
                data[key] = list(map(float, values))
    except Exception as e:
        st.error(f"Error parsing data: {e}")
    return data

# Matrix input 
def parse_matrix_input(matrix_input):
    try:
        matrix = [list(map(float, row.split(','))) for row in matrix_input.split(';')]
        return np.array(matrix)
    except Exception as e:
        st.error(f"Error parsing matrix data: {e}")
        return None

st.title('Advanced-Calci-with-Streamlit')

# Sidebar 
category = st.sidebar.selectbox('Select Category', [
    'Basic Operations', 'Root Operations',
    'Trigonometry', 'Statistics', 'Plotting', 'Matrix Operations'
])

# Main
if category == 'Basic Operations':
    st.header('Basic Operations')
    operation = st.sidebar.selectbox('Select operation', ['Addition', 'Subtraction', 'Multiplication', 'Division', 'Modulus','Exponentiation'])

    if operation in ['Addition', 'Subtraction', 'Multiplication']:
        num1 = st.number_input('Enter first number', value=0.0)
        num2 = st.number_input('Enter second number', value=0.0)
    elif operation in ['Exponentiation']:
        num1 = st.number_input('Enter base', value=0.0)
        num2 = st.number_input('Enter exponent', value=0.0)
    elif operation in ['Division', 'Modulus']:
        num1 = st.number_input('Enter Dividend', value=0.0)
        num2 = st.number_input('Enter Divisor', value=0.0)

    if st.button('Calculate'):
        if operation == 'Addition':
            result = num1 + num2
        elif operation == 'Subtraction':
            result = num1 - num2
        elif operation == 'Multiplication':
            result = num1 * num2
        elif operation == 'Division':
            if num2 != 0:
                result = num1 / num2
            else:
                result = 'Error: Division by zero'
        elif operation == 'Exponentiation':
            result = num1 ** num2
        elif operation == 'Modulus':
            result = num1 % num2
        else:
            result = "Invalid operation"

        st.write('Result:', result)

elif category == 'Root Operations':
    st.header('Root Operations')
    operation = st.sidebar.selectbox('Select operation', ['Square Root', 'Cube Root'])

    num = st.number_input('Enter number', value=0.0)

    if st.button('Calculate'):
        if operation == 'Square Root':
            result = np.sqrt(num)
        elif operation == 'Cube Root':
            result = np.cbrt(num)
        st.write('Result:', result)

elif category == 'Trigonometry':
    st.header('Trigonometric Functions')
    operation = st.sidebar.selectbox('Select function', [
        'Sine', 'Cosine', 'Tangent', 'Inverse sine', 'Inverse cosine', 'Inverse tangent'
        # ,'Hyperbolic Sine', 'Hyperbolic Cosine', 'Hyperbolic Tangent'
    ])

    num = st.number_input('Enter angle (in Degrees)', value=0.0)

    if st.button('Calculate'):
        if operation == 'Sine':
            result = np.round(np.sin(np.radians(num)), 2)
        elif operation == 'Cosine':
            result = np.round(np.cos(np.radians(num)), 2)
        elif operation == 'Tangent':
            result = np.round(np.tan(np.radians(num)), 2)
        elif operation == 'Inverse sine':
            result = np.round(np.degrees(np.arcsin(num)), 2)
        elif operation == 'Inverse cosine':
            result = np.round(np.degrees(np.arccos(num)), 2)
        elif operation == 'Inverse tangent':
            result = np.round(np.degrees(np.arctan(num)), 2)
        # elif operation == 'Hyperbolic Sine':
        #     result = np.round(np.sinh(num* np.pi/180),2)
        # elif operation == 'Hyperbolic Cosine':
        #     result = np.round(np.cosh(num* np.pi/180),2)
        # elif operation == 'Hyperbolic Tangent':
        #     result = np.round(np.tanh(num* np.pi/180),2)
        st.write('Result:', result)

elif category == 'Statistics':
    st.header('Statistical Operations')
    operation = st.sidebar.selectbox('Select statistical function', [
        'Mean', 'Median', 'Mode'
    ])

    data_input = st.text_area('Enter data (comma-separated)', value='1,2,3,4,5')

    if st.button('Calculate'):
        data = list(map(float, data_input.split(',')))
        if operation == 'Mean':
            result = np.mean(data)
        elif operation == 'Median':
            result = np.median(data)
        elif operation == 'Mode':
            try:
                result = pd.Series(data).mode().tolist()
            except:
                result = 'Error calculating mode'
        st.write('Result:', result)

elif category == 'Plotting':
    st.header('Plotting')
    plot_type = st.sidebar.selectbox('Select Plot Type', [
        'Line Plot', 'Bar Chart', 'Scatter Plot', 'Histogram', 'Pie Chart'
    ])

    if plot_type == 'Pie Chart':
        data_input = st.text_area('Enter data (e.g., labels: Category1,Category2; sizes: 10,20)', value='labels: Category1,Category2; sizes: 10,20')
        plot_data = parse_pie_data(data_input)
    elif plot_type == 'Histogram':
        data_input = st.text_area('Enter data (e.g., y: value1,value2,.....)', value='y: 34, 22, 15, 28, 37, 11, 25, 33, 14, 19, 38, 12, 40, 29, 13, 36, 30, 17, 27, 23')
        plot_data = parse_plot_data(data_input)
    else:
        data_input = st.text_area('Enter data (e.g., x: value1,value2; y: value1,value2)', value='x: Category1,Category2; y: 10,20')
        plot_data = parse_plot_data(data_input)

    if st.button('Plot'):
        fig, ax = plt.subplots()
        if plot_type == 'Line Plot':
            x = plot_data.get('x', [])
            y = list(map(float, plot_data.get('y', [])))
            ax.plot(x, y)
            ax.set_xlabel('x')
            ax.set_ylabel('y')
            ax.set_title('Line Plot')
            
        elif plot_type == 'Bar Chart':
            x = plot_data.get('x', [])
            y = list(map(float, plot_data.get('y', [])))
            ax.bar(x, y)
            ax.set_xlabel('x')
            ax.set_ylabel('y')
            ax.set_title('Bar Chart')
        
        elif plot_type == 'Scatter Plot':
            x = plot_data.get('x', [])
            y = list(map(float, plot_data.get('y', [])))
            ax.scatter(x, y)
            ax.set_xlabel('x')
            ax.set_ylabel('y')
            ax.set_title('Scatter Plot')
        
        elif plot_type == 'Histogram':
            data = list(map(float, plot_data.get('y', [])))
            ax.hist(data, bins='auto')
            ax.set_xlabel('Value')
            ax.set_ylabel('Frequency')
            ax.set_title('Histogram')
        
        # elif plot_type == 'Pie Chart':
        #     labels = plot_data.get('labels', [])
        #     sizes = plot_data.get('sizes', [])
        #     if len(labels) == len(sizes) and len(labels) > 0:
        #         ax.pie(sizes, labels=labels, autopct='%1.1f%%')
        #         ax.set_title('Pie Chart')
        #     else:
        #         st.error('The number of labels and sizes must be equal and greater than zero.')
        
        elif plot_type == 'Pie Chart':
            labels = plot_data.get('labels', [])
            sizes = plot_data.get('sizes', [])
            
            if len(labels) == len(sizes) and len(labels) > 0:
                # Calculate percentages
                total = sum(sizes)
                percentages = [f'{(size / total * 100):.1f}%' for size in sizes]
                
                # Labels/key for pie chart 
                custom_labels = [f'{label} ({percent})' for label, percent in zip(labels, percentages)]
                
                # Removing labels from chart
                wedges, _ = ax.pie(sizes, labels=None, colors=plt.get_cmap('tab20').colors)
                
                # Adding legend 
                ax.legend(wedges, custom_labels, title="Categories", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
                
                ax.set_title('Pie Chart')
            else:
                st.error('The number of labels and sizes must be equal and greater than zero.')

        
        
        else:
            st.error('Invalid plot type selected.')

        st.pyplot(fig)

elif category == 'Matrix Operations':
    st.header('Matrix Operations')
    operation = st.sidebar.selectbox('Select matrix operation', [
        'Addition', 'Subtraction', 'Multiplication', 'Determinant'
    ])

    if operation in ['Addition', 'Subtraction', 'Multiplication']:
        matrix_input1 = st.text_area('Enter first matrix (rows separated by ";" and values separated by ",")', value='1, 2; 3, 4')
        matrix_input2 = st.text_area('Enter second matrix (rows separated by ";" and values separated by ",")', value='5, 6; 7, 8')
    else:
        matrix_input1 = st.text_area('Enter a square matrix (rows separated by ";" and values separated by ",")', value='1, 2; 3, 4')
    
    if st.button('Calculate'):
        matrix1 = parse_matrix_input(matrix_input1)
        
        if operation in ['Addition', 'Subtraction', 'Multiplication']:
            matrix2 = parse_matrix_input(matrix_input2)
        
        if matrix1 is not None and (operation in ['Addition', 'Subtraction'] and matrix2 is not None):
            if operation == 'Addition':
                result = matrix1 + matrix2
            elif operation == 'Subtraction':
                result = matrix1 - matrix2
        elif matrix1 is not None and operation == 'Multiplication' and matrix2 is not None:
            result = np.dot(matrix1, matrix2)
        elif matrix1 is not None and operation == 'Determinant':
            result = np.round(np.linalg.det(matrix1), 3)
        else:
            result = 'Error: Invalid matrix input or operation'
        
        st.write('Result:')
        st.write(result)
