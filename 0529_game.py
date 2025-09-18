import random

class Attacker:
    def __init__(self, name):
        self.name = name
        self.health = 100
        self.mana = 100
        self.cooldowns = {}  # 冷卻時間記錄
        self.stun_duration = 0

    def slash(self):
        return {"name": "Slash", "damage": 10, "mana_cost": 0, "cooldown": 0}

    def fireball(self):
        if self.mana < 20 or self.cooldowns.get("fireball", 0) > 0:
            return None
        self.mana -= 20
        return {"name": "Fireball", "damage": 20, "mana_cost": 20, "cooldown": 2}

    def power_strike(self):
        if self.mana < 15 or self.cooldowns.get("power_strike", 0) > 0:
            return None
        self.mana -= 15
        return {"name": "Power Strike", "damage": 15, "mana_cost": 15, "cooldown": 1}

    def heal(self):
        if self.mana < 10 or self.cooldowns.get("heal", 0) > 0:
            return None
        self.mana -= 10
        return {"name": "Heal", "heal": 25, "mana_cost": 10, "cooldown": 2}

    def restore_mana(self):
        self.mana = min(100, self.mana + 10)

class Monster:
    def __init__(self):
        self.name = "Wild Beast"
        self.health = 150

    def claw(self):
        return {"name": "Claw", "damage": 10}

    def bite(self):
        return {"name": "Bite", "damage": 15}

    def stun(self):
        return {"name": "Stun", "damage": 0, "stun": 2}

def battle():
    attacker_name = input("請輸入攻擊者名字: ")
    attacker = Attacker(attacker_name)
    monster = Monster()
    round_count = 1

    while attacker.health > 0 and monster.health > 0:
        print(f"\n---\n回合 {round_count}")
        print(f"{attacker.name} - 血量: {attacker.health}, 魔力: {attacker.mana}")

        available_skills = [skill for skill in ["Slash", "Fireball", "Power Strike", "Heal"] if attacker.cooldowns.get(skill.lower(), 0) == 0]
        cooldowns = [f"[{skill}, 剩餘 {turns} 回合]" for skill, turns in attacker.cooldowns.items() if turns > 0]
        print(f"目前可用技能: {available_skills}")
        print(f"冷卻中: {cooldowns if cooldowns else '[]'}")
        print(f"{monster.name} - 血量: {monster.health}")

        if attacker.stun_duration > 0:
            print(f"{attacker.name} 被暈眩，無法行動！")
            attacker.stun_duration -= 1
            attack_skill = None
        else:
            while True:
                print("\n選擇技能: 1. Slash 2. Fireball 3. Power Strike 4. Heal")
                choice = input("請輸入技能編號: ")
                skill_map = {"1": attacker.slash, "2": attacker.fireball, "3": attacker.power_strike, "4": attacker.heal}
                attack_skill = skill_map.get(choice, lambda: None)()
                if attack_skill:
                    break
                print("技能無法施放！請重新選擇。")

        if attack_skill:
            if "damage" in attack_skill:
                monster.health -= attack_skill["damage"]
                print(f"{attacker.name} 使用 {attack_skill['name']}，造成 {attack_skill['damage']} 點傷害！")
                if attack_skill["cooldown"] > 0:  
                    attacker.cooldowns[attack_skill["name"].lower()] = attack_skill["cooldown"] + 1  # 下一回合開始算冷卻

            elif "heal" in attack_skill:
                attacker.health = min(100, attacker.health + attack_skill["heal"])
                print(f"{attacker.name} 使用 {attack_skill['name']}，恢復 {attack_skill['heal']} 點血量！")
                if attack_skill["cooldown"] > 0:  
                    attacker.cooldowns[attack_skill["name"].lower()] = attack_skill["cooldown"] + 1  

        monster_skill = random.choice([monster.claw, monster.bite, monster.stun])()
        print(f"{monster.name} 使用 {monster_skill['name']}！")

        if "damage" in monster_skill:
            attacker.health -= monster_skill["damage"]
            print(f"{monster.name} 造成 {monster_skill['damage']} 點傷害！")

        if "stun" in monster_skill:
            attacker.stun_duration = monster_skill["stun"]
            print(f"{attacker.name} 被暈眩 {monster_skill['stun']} 回合！")

        round_count += 1
        attacker.restore_mana()

        # 冷卻時間從下一回合開始遞減
        for skill in list(attacker.cooldowns.keys()):
            if attacker.cooldowns[skill] > 1:
                attacker.cooldowns[skill] -= 1
            else:
                del attacker.cooldowns[skill]  # 冷卻結束，從冷卻列表中移除

    winner = attacker.name if attacker.health > 0 else monster.name
    print(f"\n戰鬥結束！{winner} 勝利！")

battle()
