import random
import time

def display_welcome():
    """Выводит приветственное сообщение и правила игры."""
    print("--- ДОБРО ПОЖАЛОВАТЬ В ИГРУ БОНГО! ---")
    print("Цель: Первым набрать 100 очков.")
    print("\nПравила:")
    print("1. Бросьте два кубика.")
    print("2. Обычный бросок: сумма очков добавляется к вашему счету.")
    print("3. Дубль (кроме 3-3): Сумма удваивается и добавляется к вашему счету.")
    print("4. БОНГО! (Два кубика по 3): Ваш счет обнуляется!")
    print("--------------------------------------")
    input("Нажмите Enter, чтобы начать игру...")

def roll_dice():
    """Симулирует бросок двух кубиков и возвращает их значения."""
    die1 = random.randint(1, 6)
    die2 = random.randint(1, 6)
    return die1, die2

def play_bongo():
    """Основная функция, управляющая ходом игры."""
    player_scores = {"Игрок 1": 0, "Игрок 2": 0}
    player_names = list(player_scores.keys())
    current_player_index = 0
    target_score = 100

    while True:
        current_player_name = player_names[current_player_index]

        print(f"\n--- Ход {current_player_name} ---")
        print(f"Текущие очки: Игрок 1: {player_scores['Игрок 1']}, Игрок 2: {player_scores['Игрок 2']}")

        input(f"{current_player_name}, нажмите Enter, чтобы бросить кубики...")

        die1, die2 = roll_dice()
        print(f"Вы бросили: [{die1}] и [{die2}]")
        time.sleep(1) # Небольшая задержка для лучшего восприятия

        if die1 == 3 and die2 == 3:
            print("\n!!! БОНГО !!!")
            print(f"Упс! {current_player_name}, ваши очки сгорают!")
            player_scores[current_player_name] = 0
            time.sleep(1.5)
        elif die1 == die2:
            score_gained = (die1 + die2) * 2
            player_scores[current_player_name] += score_gained
            print(f"Дубль! Вы получаете {score_gained} очков (удвоенная сумма).")
        else:
            score_gained = die1 + die2
            player_scores[current_player_name] += score_gained
            print(f"Вы получаете {score_gained} очков.")

        print(f"Новые очки {current_player_name}: {player_scores[current_player_name]}")

        # Проверка на победу
        if player_scores[current_player_name] >= target_score:
            print(f"\nⒷⒷⒷⒷⒷⒷⒷⒷⒷⒷⒷⒷⒷⒷⒷⒷⒷⒷⒷ")
            print(f"ПОБЕДА! {current_player_name} набрал {player_scores[current_player_name]} очков и выигрывает игру!")
            print(f"ⒷⒷⒷⒷⒷⒷⒷⒷⒷⒷⒷⒷⒷⒷⒷⒷⒷⒷⒷ")
            break # Завершаем игру

        # Передача хода другому игроку
        current_player_index = (current_player_index + 1) % len(player_names)

def main():
    """Основная функция для запуска игры."""
    display_welcome()
    play_bongo()
    
    # Предложить сыграть еще раз
    while True:
        play_again = input("\nХотите сыграть еще раз? (да/нет): ").lower().strip()
        if play_again == 'да':
            print("\n--- НАЧИНАЕМ НОВУЮ ИГРУ ---")
            play_bongo()
        else:
            print("Спасибо за игру в Бонго! До свидания!")
            break

if __name__ == "__main__":
    main()
