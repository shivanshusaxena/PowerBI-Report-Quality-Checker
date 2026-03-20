import zipfile
import os, json

def extract_pbix(pbix_path):
    """Extract pbix file and return path to extracted folder"""
    extract_path = pbix_path.replace('.pbix', '_extracted')
    with zipfile.ZipFile(pbix_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)
    print(f"Extracted to: {extract_path}")
    return extract_path

def explore_report(extract_path):
    """Explore Report folder contents"""
    report_path = os.path.join(extract_path, 'Report')
    for root, dirs, files in os.walk(report_path):
        for file in files:
            filepath = os.path.join(root, file)
            size = os.path.getsize(filepath)
            print(f"{filepath} — {size} bytes")

def read_layout(extract_path):
    """Read Layout file and return sections"""
    layout_path = os.path.join(extract_path, 'Report', 'Layout')
    with open(layout_path, 'r', encoding='utf-16-le') as f:
        content = f.read()
        layout = json.loads(content)
        sections = layout['sections']
        print(f"Number of pages: {len(sections)}")
        for section in sections:
            page_name = section.get('displayName', 'Unknown')
            visuals = section.get('visualContainers', [])
            print(f"Page: '{page_name}' — {len(visuals)} visuals")
        return sections

def check_visuals_per_page(sections):
    """Check: too many visuals on a single page"""
    print("\n--- CHECK 1: Visuals Per Page ---")
    for section in sections:
        page_name = section.get('displayName', 'Unknown')
        visuals = section.get('visualContainers', [])
        count = len(visuals)
        if count > 15:
            status = "❌ FAIL — too many visuals"
        elif count > 10:
            status = "⚠️  WARNING — consider reducing"
        else:
            status = "✅ PASS"
        print(f"Page '{page_name}': {count} visuals — {status}")


def check_file_size(pbix_path):
    """Check: report file size"""
    print("\n--- CHECK 2: File Size ---")
    size_bytes = os.path.getsize(pbix_path)
    size_mb = size_bytes / (1024 * 1024)
    if size_mb > 500:
        status = "❌ FAIL — file too large"
    elif size_mb > 100:
        status = "⚠️  WARNING — consider optimizing"
    else:
        status = "✅ PASS"
    
    print(f"File size: {size_mb:.2f} MB — {status}")


def check_rls(extract_path):
    """Check: RLS is configured"""
    print("\n--- CHECK 3: Row Level Security ---")
    security_path = os.path.join(extract_path, 'SecurityBindings')
    
    with open(security_path, 'rb') as f:
        content = f.read()
    
    if len(content.strip()) > 50:
        print("✅ PASS — RLS is configured")
    else:
        print("⚠️  WARNING — No RLS configured")

def check_hidden_pages(sections):
    """Check: hidden pages in report"""
    print("\n--- CHECK 4: Hidden Pages ---")
    
    for section in sections:
        page_name = section.get('displayName', 'Unknown')
        visibility = section.get('visibility', 0)
        
        if visibility == 1:
            print(f"⚠️  WARNING — Page '{page_name}' is hidden")
        else:
            print(f"✅ PASS — Page '{page_name}' is visible")

def check_relationships(extract_path):
    """Check: many-to-many and bidirectional relationships"""
    print("\n--- CHECK 5: Relationships ---")
    
    datamodel_path = os.path.join(extract_path, 'DataModel')
    
    with open(datamodel_path, 'rb') as f:
        content = f.read()
    
    # Convert to string to search for keywords
    content_str = content.decode('utf-16-le', errors='ignore')
    
    # Search for relationship indicators
    many_to_many = content_str.count('manyToMany') + content_str.count('many_to_many')
    bidirectional = content_str.count('bothDirections') + content_str.count('bidirectional')
    
    print(f"Many-to-many relationships found: {many_to_many}")
    print(f"Bidirectional relationships found: {bidirectional}")
    
    if many_to_many > 0:
        print("❌ FAIL — Many-to-many relationships detected")
    elif bidirectional > 0:
        print("⚠️  WARNING — Bidirectional relationships detected")
    else:
        print("✅ PASS — No problematic relationships found")

# Run everything
pbix_path = "/Users/shivanshumac/Documents/Python/Projects/pbix-quality-checker/Ecommerce_report.pbix"
extract_path = extract_pbix(pbix_path)
explore_report(extract_path)
sections = read_layout(extract_path)
check_visuals_per_page(sections)
check_file_size(pbix_path)
check_rls(extract_path)
check_hidden_pages(sections)
check_relationships(extract_path)