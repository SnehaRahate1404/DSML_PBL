
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize

def summarize_text(text, num_sentences):
    sentences = sent_tokenize(text)
    stop_words = set(stopwords.words('english'))
    filtered_sentences = [sentence for sentence in sentences if any(word not in stop_words for word in sentence.split())]
    summary = ' '.join(filtered_sentences[:num_sentences])
    return summary

text="""## Cats: The Fascinating Felines

Cats are small, furry mammals that have captivated humans for thousands of years. They are known for their independent nature, playful personalities, and graceful movements. Here's a rundown of some key information about cats:

  Physical Characteristics:  

    Size:   Domestic cats range from 8 to 18 inches tall and weigh between 8 and 11 pounds, depending on breed.
    Appearance:    Cats have soft, dense fur that comes in a wide range of colors and patterns. They have sharp claws that retract into sheaths, a flexible spine, and excellent night vision.
    Lifespan:   Domestic cats typically live for 12-15 years, but some can live up to 20 years.

  Behavior:  

    Independent:   Cats are known for their independent nature and can entertain themselves for hours.
    Curious:   They are naturally curious and love to explore their surroundings.
    Playful:   Cats are playful animals and enjoy chasing toys and batting at objects.
    Nocturnal:    Cats are crepuscular, meaning they are most active at dawn and dusk, but they can be nocturnal too.
    Grooming:    Cats are meticulous groomers and spend a significant amount of time licking their fur.

  Communication:  

    Vocalizations:   Cats use a variety of vocalizations, including meows, purrs, hisses, and growls, to communicate with each other and humans.
    Body Language:    Their body language can be just as informative as their vocalizations, with postures, tail movements, and ear positions conveying different messages.

  Diet:

    Carnivores:   Cats are obligate carnivores, meaning they require meat in their diet.
    Commercial Cat Food:   A balanced commercial cat food provides all the nutrients they need.
    Treats:   Treats should be given in moderation, as they can lead to weight gain.

  Health:

    Vaccinations:   Cats should be vaccinated against common diseases such as rabies, feline distemper, and feline leukemia.
    Parasites:   Cats can be susceptible to parasites like fleas, ticks, and intestinal worms.
    Health Checkups:   Regular veterinary checkups are crucial for maintaining their health.

  Breeds:

There are over 70 recognized cat breeds, each with unique physical characteristics and personality traits. Some popular breeds include:

    Siamese:   Known for their striking blue almond-shaped eyes and distinctive Siamese pattern.
    Persian:    Characterized by their long, luxurious fur and sweet, docile temperament.
    Maine Coon:    The largest domestic cat breed, with a thick, fluffy coat and a friendly personality.
    Scottish Fold:    Known for their unique folded ears and playful nature.
    Ragdoll:    Affectionate cats with a relaxed, docile temperament.

  Cats in History and Culture:

Cats have played a significant role in human history and culture.  They have been revered as gods in ancient Egypt, worshipped in some cultures, and featured in numerous works of art and literature.

  Cats make wonderful companions:   They can provide comfort, companionship, and endless entertainment. If you are considering adopting a cat, research different breeds and shelters to find the perfect feline friend for you."""
summary = summarize_text(text, 2)
print(summary)
