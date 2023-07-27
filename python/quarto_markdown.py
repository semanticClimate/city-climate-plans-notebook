import os
from markdownify import markdownify
from bs4 import BeautifulSoup
import re

# variables
input_directory = '/Users/ad7588/projects/semanticclimate/semanticclimate_input'
output_directory = '/Users/ad7588/projects/semanticclimate/semanticclimate_output'
quarto_directory = '/Users/ad7588/projects/semanticclimate'

# function to transform HTML to Markdown
def html_to_markdown(html):
    soup = BeautifulSoup(html, 'html.parser')
    
    # remove <head> section from the soup
    head = soup.head
    if head is not None:
        head.decompose()
    
    # process the HTML to apply styles from the head directly to the HTML
    soup = process_html(soup)

    # convert HTML to Markdown
    markdown = markdownify(soup, heading_style='UNDERLINED', sub_symbol='~')
    
    # process the Markdown to tidy up various processing issues
    markdown = process_markdown(markdown)

    return markdown

# function to process HTML
def process_html(soup):
    soup = soup.prettify()

    # for debugging: write new HTML file
    html_file = output_directory + '/prettified.html'
    with open(html_file, 'w') as f:
        f.write(soup)

    # change first classref s0 span into a <h1>
    soup = re.sub(r'<span class="s0"[^>]*>([\s\S]*?)<\/span>', r'<h1>\1</h1>', soup, count=1)
    # changing bold classrefs to <strong>
    soup = re.sub(r'<span class="s0"[^>]*>([\s\S]*?)<\/span>', r'<strong>\1</strong>', soup)
    soup = re.sub(r'<span class="s183"[^>]*>([\s\S]*?)<\/span>', r'<strong>\1</strong>', soup)
    soup = re.sub(r'<span class="s1040"[^>]*>([\s\S]*?)<\/span>', r'<strong>\1</strong>', soup)
    soup = re.sub(r'<span class="s1962"[^>]*>([\s\S]*?)<\/span>', r'<strong>\1</strong>', soup)
    soup = re.sub(r'<span class="s2054"[^>]*>([\s\S]*?)<\/span>', r'<strong>\1</strong>', soup)
    # changing italic classrefs to <i>
    soup = re.sub(r'<span class="s107"[^>]*>([\s\S]*?)<\/span>', r'<i>\1</i>', soup)
    soup = re.sub(r'<span class="s1002"[^>]*>([\s\S]*?)<\/span>', r'<i>\1</i>', soup)
    soup = re.sub(r'<span class="s1013"[^>]*>([\s\S]*?)<\/span>', r'<strong><i>\1</i></strong>', soup)
    soup = re.sub(r'<span class="s1050"[^>]*>([\s\S]*?)<\/span>', r'<i>\1</i>', soup)
    # changing smallest fontsize classrefs to <sub>
    soup = re.sub(r'<span class="s101"[^>]*>([\s\S]*?)<\/span>', r'<sub>\1</sub>', soup)
    soup = re.sub(r'<span class="s1000"[^>]*>([\s\S]*?)<\/span>', r'<sub>\1</sub>', soup)
    soup = re.sub(r'<span class="s1011"[^>]*>([\s\S]*?)<\/span>', r'<strong><sub>\1<sub></strong>', soup)
    soup = re.sub(r'<span class="s1044"[^>]*>([\s\S]*?)<\/span>', r'<sub>\1</sub>', soup)
    soup = re.sub(r'<span class="s1969"[^>]*>([\s\S]*?)<\/span>', r'<sub>\1</sub>', soup)
    # changing largest fontsize classrefs to <h1>
    soup = re.sub(r'<span class="s113"[^>]*>([\s\S]*?)<\/span>', r'<h1>\1</h1>', soup)
    soup = re.sub(r'<div style="font-size: 20px;[^>]*>([\s\S]*?)<\/div>', r'<h1>\1</h1>', soup)
    # changing div 'section' headings to <h2>
    soup = re.sub(r'<div class="section"[^>]*>([\s\S]*?)<\/div>', r'<h2>\1</h2>', soup)
    # changing div 'sub_section' headings to <h3>
    soup = re.sub(r'<div class="sub_section"[^>]*>([\s\S]*?)<\/div>', r'<h3>\1</h3>', soup)

    # for debugging: write new HTML file
    html_file = output_directory + '/processed.html'
    with open(html_file, 'w') as f:
        f.write(soup)

    return soup

# Function to process Markdown
def process_markdown(markdown):

    markdown = re.sub(r'\*\* \n\*\*', r'', markdown)
    markdown = re.sub(r'\n \n~', r'~', markdown)
    markdown = re.sub(r'~ \n\n ', r'~', markdown)
    markdown = re.sub(r'\n \n\*', r' *', markdown)
    markdown = re.sub(r'\* \n\n', r'*', markdown)
    markdown = re.sub(r'### \n', r'### ', markdown)

    return markdown

# MAIN PROGRAM
# iterate over files in the input directory
for subdir, dirs, files in os.walk(input_directory):
    for file in files:
        # file name with extension
        file_name = os.path.basename(file)
        read_file = subdir + '/' + file_name

        # read HTML file
        html = open(read_file, "r").read()

        markdown = html_to_markdown(html)

        # write Markdown file
        write_file = quarto_directory + '/' + os.path.splitext(file)[0] + '.qmd'
        with open(write_file, 'w') as f:
            f.write(markdown)