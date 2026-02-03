from armourbound_guardian import ArmourboundGuardianAI


def main():
    ai = ArmourboundGuardianAI()
    steps = ai.plan_moon_mission()
    for i, s in enumerate(steps, 1):
        print(f"{i}. {s}")


if __name__ == '__main__':
    main()
