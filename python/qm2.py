import requests
from bs4 import BeautifulSoup
from markdownify import markdownify

# Function to retrieve the CSS styles from the <head> section of HTML
def get_css_styles(soup):
    styles = []
    head = soup.head
    if head is not None:
        for style_tag in head.find_all('style'):
            styles.append(style_tag.get_text())
    return styles

# Function to transform HTML to Markdown and insert class references
def html_to_markdown(html):
    soup = BeautifulSoup(html, 'html.parser')

    # Retrieve CSS styles from <head> section
    css_styles = get_css_styles(soup)

    # Remove <head> section from the soup
    head = soup.head
    if head is not None:
        head.decompose()

    # Convert HTML to Markdown
    markdown = markdownify(str(soup), heading_style='ATX')

    # Insert class references into the HTML tags
    for css_style in css_styles:
        style_lines = css_style.strip().split('\n')
        for style_line in style_lines:
            style_line = style_line.strip()
            if not style_line.startswith(('/*', '*/')):
                classref = style_line.split('{')[0].strip()
                elements = soup.select(classref)
                for element in elements:
                    element['class'] = classref[1:]  # Remove the leading dot

    # Return the transformed Markdown
    return markdown

# Example usage
read_file = '/Users/ad7588/projects/semanticclimate/semanticclimate_input' + '/groups_groups.html'
html = open(read_file, "r").read()

markdown = html_to_markdown(html)

# write new Markdown file
write_file = '/Users/ad7588/projects/semanticclimate/semanticclimate_input' + '/new.qmd'
with open(write_file, 'w') as f:
    f.write(markdown)
