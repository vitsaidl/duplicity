# Program na hledání duplicit/unikátních hodnot 
Program slouží k nalezení buďto unikátních, anebo duplicitních záznamů v csv-like souboru. Jako separátor sloupečků lze nastavit nejenom čárku, ale i tečku, mezeru, lomítko a řadu dalších znaků. Program dokáže pracovat i v případě, kdy csvčku chybí hlavička nebo tato hlavička není kompletní.
Při práci se nejprve musí nastavit separátor, kódování (defaultní je utf-8) a hlavička. Posléze se tlačítkem "Nahraj soubor" csvčko nahraje a v textovém poli se objevý krátký report. V comboboxu pod tím vybereme, nad kterými sloupci dat chceme duplicity hledat. Následně zvolíme, zda duplicitním záznamem myslíme druhý výskyt (a další výskyty) řádku, který se nacházel v souboru již dříve, anebo i první výskyt daného záznamu. Nakonec zvolíme, zda chceme znát unikátní, nebo duplicitní řádky, a kliknutím na tlačítko úplně dole se nám ve stejném adresáři, ve kterém je pythoní program, vytvoří výsledný soubor s unikáty/duplicitami.
Pro otestování funkce programu je v repozitáři umístěný malý csv soubor - pokusna_data.csv.

Jedná se o pythoní program, takže exe soubor bohužel poskytnout nemohu. Jednou z možností, jak program spustit, je nějaké IDE (např Spyder v Anakondě). Jelikož spouštění IDE může být občas nešikovné/zbytečné, je v adresáři i baťák obstarávající spuštění pythonu. Před použitím bude nutné přepsat cestu vedoucí k souboru python.exe. Pakliže máte na počítači Anacodnu, mělo by na odpovídající místě být něco jako C:\Users\jmenoUzivatele\Appdata\Local\Continuum\anaconda3\python.exe.

Historie
18. 11. 18 - první verze programu
20. 11. 18 - přidání podpory mezer coby oddělovačů a neexistující hlavičky, rozhraní udělané více user-friendly
21. 11. 18 - přidání volby kódování
25. 11. 18 - přidání informování uživatele o tom, kam se uložil výsledný soubor + zpřehlednění kódu (obé napsal Miloslav Létal), přidání možnosti odebrat číslování řádků (+ řádky se nyní číslují ne od 0, ale od 1), seznam sloupců, nad kterými se hledají duplicity, už není v comboboxu, ale v listboxu