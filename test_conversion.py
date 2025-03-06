"""
Quick test script for the transliteration mapper.
"""

from transliteration.mapper import TransliterationMapper

def main():
    mapper = TransliterationMapper()
    
    # Test texts from the examples
    test_texts = [
        # Test Text 1
        "Salam 3likom, kidayr a sa7bi? Wach kolchi bikhir?\nLbar7 kont f su9 w tla9it m3a wahd sahibna, gal liya 3la chi khbr mzyan!\nYalah jibi 7aja nshrboha f café, kayn chi mochkila?",
        
        # Test Text 2
        "Ch7al f had l'prix? 3afak goliya wach hadchi normal?\nKhasni chi haja pour mon projet, mais ma3rfch mnin njibha!\nRani tired bzaf, kantfkr nji l'3tla nchoufkom!",
        
        # Test Text 3
        "Fink a zin? Wach mazal 3ndek dakchi lli golti?\nSma7 liya a khti, rani mchghoul daba, ndir lik call mn b3d inchallah!\nMachi mochkil, nchofkom m3a l3achiya!",
        
        # Test Text 4
        "Hadi chi 9adia kbira, 3ad fhmto daba!\nSafi, rani 7ader, yalah ndiro chi planning l had lyoum.\nDaba ghadi nmchi l 7omm lqdim bach nchouf chi 7wayj."
    ]
    
    # Convert each test text
    for i, text in enumerate(test_texts):
        print(f"\n=== Test Text {i+1} ===")
        print("Original:")
        print(text)
        print("\nConverted:")
        converted = mapper.convert(text)
        print(converted)
        print("\n")
    
if __name__ == "__main__":
    main()
