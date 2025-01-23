import random

# Defines the usable characters and their stats
characters = [
    {"name": "Astra", "hp": 100, "max_hp": 100, "attack": 15, "ability": "Solar Burst", "rarity": "Legendary", "experience": 0, "skill_points": 5},
    {"name": "Orion", "hp": 80, "max_hp": 80, "attack": 20, "ability": "Meteor Strike", "rarity": "Rare", "experience": 0, "skill_points": 5},
    {"name": "Nova", "hp": 70, "max_hp": 70, "attack": 10, "ability": "Nova Wave", "rarity": "Common", "experience": 0, "skill_points": 5},
    {"name": "Lucia", "hp": 120, "max_hp": 120, "attack": 12, "ability": "Thunder Strike", "rarity": "Epic", "experience": 0, "skill_points": 5},
    {"name": "Zephyr", "hp": 90, "max_hp": 90, "attack": 18, "ability": "Wind Slash", "rarity": "Rare", "experience": 0, "skill_points": 5},
    {"name": "Traveler", "hp": 40, "max_hp": 40, "attack": 5, "ability": "Basic Slash", "rarity": "Common", "experience": 0, "skill_points": 5}  # Traveler is starting character
]

# Defines the enemies and their stats
enemies = [
    {"name": "Cosmic Raider", "hp": 60, "max_hp": 60, "attack": 8, "ability": "Plasma Shot", "rarity": "Common", "experience": 0},
    {"name": "Galactic Bandit", "hp": 80, "max_hp": 80, "attack": 12, "ability": "Laser Slash", "rarity": "Rare", "experience": 0},
    {"name": "Void Sentinel", "hp": 100, "max_hp": 100, "attack": 15, "ability": "Dark Pulse", "rarity": "Legendary", "experience": 0}
]

# Gacha system to summon characters
def gacha_system(gems):
    print(f"\nYou have {gems} gems.")
    if gems >= 100:
        print("You can summon a character!")
        # 80% chance of Common, 15% Rare, 5% Legendary
        rarity = random.choices(["Common", "Rare", "Legendary"], [0.8, 0.15, 0.05])[0]
        available_characters = [char for char in characters if char["rarity"] == rarity]
        new_character = random.choice(available_characters)
        print(f"You've summoned {new_character['name']}, a {new_character['rarity']} character!")
        return new_character
    else:
        print("You don't have enough gems to summon a character.")
        return None

# This makes the attack system more dynamic by adding a chance to miss
def attack_miss(chance_to_miss):
    return random.random() < chance_to_miss

# Battle system where the player and enemy take turns attacking
def battle(player, battle_count):
    # Randomly select an enemy from the enemy list
    enemy = random.choice(enemies)
    enemy["hp"] = enemy["max_hp"]  # Reset the enemy's HP to full
    
    print(f"\nBattle Started: {player['name']} vs {enemy['name']}")
    
    # Scale enemy stats based on the battle count (making early battles easier)
    if battle_count < 3:  # The first 3 battles will be easier
        enemy["hp"] = random.randint(20, 40)
        enemy["attack"] = random.randint(3, 6)
    else:
        enemy["hp"] += battle_count * 5  # Increase HP per battle won after the 3rd battle
        enemy["attack"] += battle_count // 2  # Increases attack every 2 battles
    

    # Battle loop: player and enemy take turns
    while player["hp"] > 0 and enemy["hp"] > 0:
        # Display health, level, experience bar, and skill points
        print("\n----------------------------")
        print(f"{player['name']} (Level {player['experience'] // 100 + 1}) *")  # Added * to indicate player
        print(f"HP: {player['hp']} / {player['max_hp']}")  # Display current HP / max HP of the player
        print(f"Attack: {player['attack']} | Skill Points: {player['skill_points']}")
        experience_bar = '=' * (player["experience"] // 10) + ' ' * (10 - player["experience"] // 10)
        print(f"Experience: [{experience_bar}] {player['experience']} / 100")
        print("----------------------------")
        print(f"{enemy['name']} (Level {enemy['experience'] // 100 + 1})")
        print(f"HP: {enemy['hp']} / {enemy['max_hp']}")  # Display current HP / max HP of the enemy
        print(f"Attack: {enemy['attack']}")
        print("----------------------------")
        
        # Battle actions
        print("\nBattle Actions:")
        print("1. Attack")
        print("2. Use Ability")
        print("\n3. Run")
        # Using a try-except block to handle invalid inputs
        try:
            action = input("Choose an action (1-3): ")
            if action == "1":
                # Basic Attack
                if attack_miss(0.02):  # 2% chance to miss basic attack
                    print(f"{player['name']}'s attack missed!")
                else:
                    damage = random.randint(player["attack"], player["attack"] * 2)
                    enemy["hp"] -= damage
                    player["skill_points"] = min(player["skill_points"] + 1, 5)  # Recover 1 skill point, max 5
                    print(f"{player['name']} attacks {enemy['name']} for {damage} damage!")
            
            elif action == "2":
                # Use Ability, requires 2 skill points
                if player["skill_points"] >= 2:
                    if attack_miss(0.04):  # 4% chance to miss ability
                        print(f"{player['name']} missed using {player['ability']}!")
                    else:
                        damage = random.randint(player["attack"] * 2, player["attack"] * 4)  # Ability deals more damage
                        enemy["hp"] -= damage
                        player["skill_points"] -= 2  # Consume 2 skill points
                        print(f"{player['name']} uses {player['ability']} on {enemy['name']} for {damage} damage!")
                else:
                    print(f"{player['name']} doesn't have enough skill points for ability!")

            elif action == "3":
                print(f"{player['name']} ran away!")
                return "Player ran away"
            
            # Enemy attacks back
            if enemy["hp"] > 0:
                if attack_miss(0.02):  # 2% chance to miss enemy basic attack
                    print(f"{enemy['name']}'s attack missed!")
                else:
                    damage = random.randint(enemy["attack"], enemy["attack"] * 2)
                    player["hp"] -= damage
                    print(f"{enemy['name']} attacks {player['name']} for {damage} damage!")

            # Check if someone is defeated
            if player["hp"] <= 0:
                print(f"\n{player['name']} has been defeated!")
                player["hp"] = player["max_hp"]  # Heal immediately when defeated
                print(f"{player['name']}'s HP has been restored!")
                return "Player lost"
            elif enemy["hp"] <= 0:
                print(f"\n{enemy['name']} has been defeated!")
                player["experience"] += 20
                if player["experience"] >= 100:
                    player["experience"] -= 100
                    player["hp"] = player["max_hp"]  # Restore max HP on level up
                    player["attack"] += 2
                    print(f"{player['name']} leveled up! New HP: {player['hp']}, New Attack: {player['attack']}")
                return "Player won"
        except KeyboardInterrupt:
            print("Invalid input. Please enter a number.")

    # Replenish HP after each battle
    print(f"\n{player['name']}'s HP has been replenished after the battle!")
    player["hp"] = player["max_hp"]  # Set player's HP to full after each battle

# Game loop to run the game
def game():
    # Introducing the game's lore
    print("Welcome to *Horizon Star Voyage*!")
    print("\n--- Lore Introduction ---")
    print(""" 
    In the distant future, humanity has embarked on a journey beyond the stars, leaving Earth behind to explore the vast unknown. 
    The galaxy is a vast expanse filled with wonders, dangers, and ancient mysteries. Among the stars, various factions have risen, 
    each vying for power, knowledge, and control over the cosmos.

    You are a young adventurer, a rising star in the "Horizon Fleet," a group dedicated to exploring and safeguarding the distant reaches of space.
    As a member of the Horizon Fleet, your mission is simple: chart unknown worlds, uncover lost technologies, and protect humanity from the dangers lurking beyond.

    However, as you venture deeper into the galaxy, you will soon discover that not all is as it seems. Strange entities, powerful artifacts, and ancient secrets 
    lie waiting to be uncovered, and with them come challenges that could alter the course of history.

    Will you become a hero among the stars, or will the vastness of space swallow you whole? Your journey begins now in *Horizon Star Voyage*.
    """)
    input("Press Enter to begin your journey...")

    gems = 50  # Starting gems for the player
    print("\nYou have 50 gems to start with!")

    # You will start the game as the Traveler character
    player = characters[5]  # Traveler character starts the game
    player["hp"] = player["max_hp"]  # Ensure player starts with max HP
    print(f"You start the game as {player['name']}!")

    battle_count = 0  # Tracker for how many wins the player has
    
    while True:
        # Main menu for the game
        print("\n--- Main Menu ---")
        print(f"Current Gems: {gems}")  
        print("1. Fight Enemy")
        print("2. Use Gacha System")
        print("3. View Player Stats")
        print("4. Rest (Heal and Recover Skill Points)")
        print("5. Exit")
        try:
            choice = input("Enter your choice (1-5): ")
        
            if choice == "1":
                # Start a battle
                result = battle(player, battle_count)
                if result == "Player won":
                    gems += 50  # Earn gems for winning
                    battle_count += 1  # Increase battle count after winning
            elif choice == "2":
                # Use Gacha to summon a character
                new_character = gacha_system(gems)
                if new_character:
                    player = new_character
                    gems -= 100  # Spend 100 gems to summon a new character
            elif choice == "3":
                # View player stats
                print("\nPlayer Stats:")
                print(f"Name: {player['name']}")
                print(f"HP: {player['hp']} / {player['max_hp']}")
                print(f"Attack: {player['attack']}")
                print(f"Skill Points: {player['skill_points']}")
                print(f"Experience: {player['experience']} / 100")
            elif choice == "4":
                # Rest to heal and recover skill points
                player["hp"] = player["max_hp"]
                player["skill_points"] = 5  
                print(f"{player['name']} has rested and is fully healed, with skill points restored!")
            elif choice == "5":
                print("Thanks for playing! Goodbye.")
                break
            else:
                print("Invalid choice. Please try again.")
        except KeyboardInterrupt:
            print("Invalid input. Please enter a number.")

# Start the game
try:
    game()
except KeyboardInterrupt:
    print("Why would you interrupt such a great game?")
    
