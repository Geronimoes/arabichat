"""
Test script to evaluate the transliteration of Arabic chat to Arabica.
"""

from transliteration.mapper import TransliterationMapper

def test_transliteration():
    """Test the transliteration with various examples."""
    mapper = TransliterationMapper()
    
    # Test cases
    test_cases = [
        # Test 1: General Conversation
        "Salam 3likom, kidayr a sa7bi? Wach kolchi bikhir?",
        "Lbar7 kont f su9 w tla9it m3a wahd sahibna, gal liya 3la chi khbr mzyan!",
        "Yalah jibi 7aja nshrboha f café, kayn chi mochkila?",
        
        # Test 2: Casual Chat with Mixed English & French Words
        "Ch7al f had l'prix? 3afak goliya wach hadchi normal?",
        "Khasni chi haja pour mon projet, mais ma3rfch mnin njibha!",
        "Rani tired bzaf, kantfkr nji l'3tla nchoufkom!",
        
        # Test 3: More Dialectal Expressions & Shortcuts
        "Fink a zin? Wach mazal 3ndek dakchi lli golti?",
        "Sma7 liya a khti, rani mchghoul daba, ndir lik call mn b3d inchallah!",
        "Machi mochkil, nchofkom m3a l3achiya!",
        
        # Test 4: Spoken Moroccan Chat with Abbreviations & Numbers
        "Hadi chi 9adia kbira, 3ad fhmto daba!",
        "Safi, rani 7ader, yalah ndiro chi planning l had lyoum.",
        "Daba ghadi nmchi l 7omm lqdim bach nchouf chi 7wayj."
    ]
    
    # Convert and display each test case
    for i, test in enumerate(test_cases, 1):
        result = mapper.convert(test)
        print(f"Test {i}: {test}")
        print(f"Result: {result}")
        print("-" * 80)

if __name__ == "__main__":
    test_transliteration()
