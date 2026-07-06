# VibeCoding: this demo was co-developed with AI assistance

# to simulate a multi-agent negotiation process in heating dispatch.

"""

供热调度 - 多Agent协商（四轮，双方互让，向中间靠拢）

角色：

- 民生代表：目标室温 ≥ 22°C，但愿意逐步下调以降低成本。

- 效益代表：目标室温 ≥ 18°C（最低），希望尽量降低成本，但愿意接受略高室温以保民生。

评分：民生分（室温18°C以下指数锐减）、效益分（成本指数衰减），综合得分 = 几何平均。

机制：每轮双方各提建议，Leader 从当前、民生建议、效益建议中选综合得分最高者。

"""



import math



# ---------- 数据结构 ----------

class Plan:

    def __init__(self, source, supply_temp, cost, room_temp, agent=""):

        self.source = source

        self.supply_temp = supply_temp

        self.cost = cost

        self.room_temp = room_temp

        self.agent = agent



# ---------- 边际递减评分 ----------

def welfare_score(room_temp):

    if room_temp >= 18.0:

        return 100.0

    delta = 18.0 - room_temp

    return 100.0 * math.exp(-0.12 * delta * delta)



def economic_score(cost):

    return 100.0 * math.exp(-0.025 * cost)



def combined_score(plan):

    w = welfare_score(plan.room_temp)

    e = economic_score(plan.cost)

    return math.sqrt(w * e) if w > 0 and e > 0 else 0



# ---------- 基类 ----------

class Agent:

    def __init__(self, name):

        self.name = name



# ---------- 领导 ----------

class Leader(Agent):

    def __init__(self, weather, demands):

        super().__init__("总调度")

        self.weather = weather

        self.demands = demands

        self.min_room = 18.0



    def apply_suggestion(self, plan, sugg, agent_name):

        new_source = plan.source + sugg.get('source', 0)

        new_supply = {}

        for s, temp in plan.supply_temp.items():

            adj = sugg.get('supply', {}).get(s, 0)

            new_supply[s] = max(70, temp + adj)



        total_demand = sum(d['base'] for d in self.demands)

        new_cost = new_source * 0.8 + 0.2 * sum(abs(new_supply[s] - plan.supply_temp[s]) for s in new_supply)

        new_room = 18.0 + (new_source - total_demand) * 0.02



        # 硬约束 ：不低于18°C

        if new_room < self.min_room:

            deficit = self.min_room - new_room

            new_source += deficit * 2.0

            for s in new_supply:

                new_supply[s] += deficit * 0.5

            new_room = self.min_room

            new_cost += deficit * 1.5



        return Plan(new_source, new_supply, new_cost, new_room, agent_name)



    def start_negotiation(self, welfare_agent, economy_agent, rounds=4):

        print(f"\n{self.name}: 各位，今天室外 {self.weather['temp']}°C，共 {len(self.demands)} 个换热站。")

        print(f"民生底线 18°C，请双方提出初始预案。\n")



        # 初始极端方案

        w_plan = welfare_agent.initial_plan(self.weather, self.demands)

        e_plan = economy_agent.initial_plan(self.weather, self.demands)



        # 初始选综合分较高者（通常民生更高，但先比较）

        current = w_plan if combined_score(w_plan) >= combined_score(e_plan) else e_plan

        print(f"【初始】采用 {current.agent} 的预案：")

        print(f"  出力 {current.source:.1f} GJ/h，成本 {current.cost:.1f} 万元，室温 {current.room_temp:.1f}°C")

        print(f"  民生评分 {welfare_score(current.room_temp):.1f}，效益评分 {economic_score(current.cost):.1f}，综合 {combined_score(current):.1f}\n")



        history = [current]



        for r in range(1, rounds + 1):

            print(f"--- 第 {r} 轮协商 ---")

            # 双方各提建议（向自己目标调整）

            w_sugg = welfare_agent.suggest(current)

            e_sugg = economy_agent.suggest(current)



            print(f"  {welfare_agent.name}: 我建议将出力 {'提高' if w_sugg['source']>0 else '降低'} {abs(w_sugg['source']):.1f}，供水各站上调 {w_sugg['supply']}，力争室温接近 22°C。")

            print(f"  {economy_agent.name}: 我建议将出力 {'提高' if e_sugg['source']>0 else '降低'} {abs(e_sugg['source']):.1f}，供水各站下调 {e_sugg['supply']}，控制成本，室温维持在 18°C 以上即可。")



            # 生成候选

            w_candidate = self.apply_suggestion(current, w_sugg, "民生建议")

            e_candidate = self.apply_suggestion(current, e_sugg, "效益建议")



            candidates = [current, w_candidate, e_candidate]

            scores = [combined_score(p) for p in candidates]

            best_idx = scores.index(max(scores))

            best_plan = candidates[best_idx]

            best_agent = ["当前", "民生建议", "效益建议"][best_idx]



            print(f"\n  评估结果：")

            print(f"    民生建议方案 -> 室温 {w_candidate.room_temp:.1f}°C，成本 {w_candidate.cost:.1f} 万，综合 {scores[1]:.1f}")

            print(f"    效益建议方案 -> 室温 {e_candidate.room_temp:.1f}°C，成本 {e_candidate.cost:.1f} 万，综合 {scores[2]:.1f}")

            print(f"    当前方案       -> 室温 {current.room_temp:.1f}°C，成本 {current.cost:.1f} 万，综合 {scores[0]:.1f}")

            print(f"  {self.name}: 本轮采纳 {best_agent}，新方案综合得分 {scores[best_idx]:.1f}。")



            current = best_plan

            history.append(current)



            if combined_score(current) >= 95:

                print("  综合评分已极高，协商提前结束。")

                break



        final = max(history, key=combined_score)

        print(f"\n{self.name}: 经四轮协商，最终决定采用以下预案（综合评分 {combined_score(final):.1f}）：")

        return final



# ---------- 民生代表 ----------

class WelfareAgent(Agent):

    def __init__(self):

        super().__init__("民生代表")



    def initial_plan(self, weather, demands):

        total = sum(d['base'] for d in demands)

        source = total * 1.4          # 高供热，室温约 22.4°C

        supply = {d['id']: 105.0 for d in demands}

        cost = source * 0.95

        room = 22.4

        return Plan(source, supply, cost, room, self.name)



    def suggest(self, plan):

        # 如果当前室温低于22°C，则建议升温（增加出力）

        if plan.room_temp < 22.0:

            return {'source': 2.0, 'supply': {s: 1.0 for s in plan.supply_temp}}

        else:

            # 如果已经达到或超过22，则不再继续升温（可适当保持）

            return {'source': 0.0, 'supply': {}}



# ---------- 效益代表 ----------

class EconomyAgent(Agent):

    def __init__(self):

        super().__init__("效益代表")



    def initial_plan(self, weather, demands):

        total = sum(d['base'] for d in demands)

        source = total * 0.9          # 低供热，室温约 18.0°C

        supply = {d['id']: 75.0 for d in demands}

        cost = source * 0.65

        room = 18.0

        return Plan(source, supply, cost, room, self.name)



    def suggest(self, plan):

        # 如果当前室温高于18°C，则建议降温（减少出力以节本）

        if plan.room_temp > 18.0:

            return {'source': -2.0, 'supply': {s: -1.0 for s in plan.supply_temp}}

        else:

            # 如果已经达到18底线，则不再继续降

            return {'source': 0.0, 'supply': {}}



# ---------- 主程序 ----------

def main():

    weather = {'temp': -5.0, 'wind': 3.5}

    demands = [{'id': 'A', 'base': 40}, {'id': 'B', 'base': 30}, {'id': 'C', 'base': 25}]



    leader = Leader(weather, demands)

    welfare = WelfareAgent()

    economy = EconomyAgent()



    final = leader.start_negotiation(welfare, economy, rounds=4)



    print("\n===== 最终调度预案 =====")

    print(f"热源出力: {final.source:.1f} GJ/h")

    print(f"各站供水温度: {final.supply_temp}")

    print(f"运行成本: {final.cost:.2f} 万元")

    print(f"预测最低室温: {final.room_temp:.1f} °C")

    print(f"民生评分: {welfare_score(final.room_temp):.1f}")

    print(f"效益评分: {economic_score(final.cost):.1f}")

    print(f"综合评分: {combined_score(final):.1f}")



if __name__ == "__main__":

    main()
