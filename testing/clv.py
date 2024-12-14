import difflib
import re
import html

class TextComparator:
    @staticmethod
    def generate_html_report(text1, text2, output_file='text_comparison_report.html'):
        words1 = text1.lower().split()
        words2 = text2.lower().split()
        matcher = difflib.SequenceMatcher(None, words1, words2)       
        marked_words2 = words2.copy()        
        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            print((tag,i1, i2, j1, j2))
            if tag != 'equal':
                for j in range(j1, j2):
                    marked_words2[j] = f'<span id="wrong" style="color:red;">{marked_words2[j]}</span>'
        
        marked_text2 = ' '.join(marked_words2)
        
        similarity_ratio = matcher.ratio()
        
       
        return marked_text2, similarity_ratio

# Example usage
def main():
    original_text = "je vais voir ma mère grand, et lui porter une galette avec un pot de beurre, que ma mère lui envoie"
    compared_text = "je vais voir ma mergrand et lui porter une galette avec empo de beure que ma mère lui envoyer."
    
    # Generate HTML report
    report_file = TextComparator.generate_html_report(original_text, compared_text)
    

if __name__ == "__main__":
    main()