"""
GameEngine: owns the frog and all vehicles and runs one frame of game logic.
"""

import random

import pygame

from game.frog import Frog
from game.vehicle import Vehicle
from game.collisions import check_collision
from game.renderer import (
    GRID_COLS,
    GOAL_ROW,
    ROAD_ROWS,
    START_ROW,
    CELL_SIZE,
    WIDTH,
    HEIGHT,
)

LANE_SPEEDS = [1.5, -2, 2, -2.5, 1.5, -2]
STARTING_LIVES = 3
STARTING_SCORE = 0
ATTEMPT_TIME = 30.0
HIT_DISPLAY_TIME = 0.35


class GameEngine:
    def __init__(self):
        self._reset_game()

    def _reset_game(self):
        self.lives = STARTING_LIVES
        self.score = STARTING_SCORE
        self.time_remaining = ATTEMPT_TIME
        self.game_active = True
        self.won = False
        self.game_over = False
        self.transition_timer = 0.0
        self.transition_message = ""
        self._last_time_ms = pygame.time.get_ticks()
        self._build_entities()

    def _build_entities(self):
        start_col = GRID_COLS // 2
        self.frog = Frog(
            col=start_col,
            row=START_ROW,
            start_col=start_col,
            start_row=START_ROW,
            cols=GRID_COLS,
            start_row_limit=START_ROW,
        )

        frog_x_range = (start_col * CELL_SIZE, start_col * CELL_SIZE + CELL_SIZE)
        self.vehicles = []

        for i, row in enumerate(ROAD_ROWS):
            speed = LANE_SPEEDS[i % len(LANE_SPEEDS)]
            vehicle_width = 40 if i % 2 == 0 else 70
            spacing = 300
            count = 2

            for _attempt in range(20):
                phase = random.randint(0, spacing - 1)
                positions = []
                safe = True

                for n in range(count):
                    offset = phase + n * spacing
                    x = offset if speed > 0 else WIDTH - offset - vehicle_width
                    positions.append(x)
                    if not (
                        x + vehicle_width <= frog_x_range[0]
                        or x >= frog_x_range[1]
                    ):
                        safe = False

                if safe:
                    break

            for x in positions:
                self.vehicles.append(
                    Vehicle(
                        x=x,
                        row=row,
                        width=vehicle_width,
                        height=CELL_SIZE - 8,
                        speed=speed,
                    )
                )

    def _start_failure_transition(self, message):
        self.game_active = False
        self.transition_message = message
        self.transition_timer = HIT_DISPLAY_TIME

    def _finish_failure(self):
        self.lives -= 1
        self.transition_timer = 0.0
        self.transition_message = ""

        if self.lives <= 0:
            self.lives = 0
            self.game_over = True
            self.game_active = False
            return

        self.frog.reset()
        self.time_remaining = ATTEMPT_TIME
        self.game_active = True
        self._last_time_ms = pygame.time.get_ticks()

    def handle_keydown(self, key):
        if key == pygame.K_r:
            self._reset_game()
            return

        if not self.game_active:
            return

        if key == pygame.K_UP:
            self.frog.move(0, -1)
        elif key == pygame.K_DOWN:
            self.frog.move(0, 1)
        elif key == pygame.K_LEFT:
            self.frog.move(-1, 0)
        elif key == pygame.K_RIGHT:
            self.frog.move(1, 0)

    def update(self):
        now_ms = pygame.time.get_ticks()
        dt = max(0.0, (now_ms - self._last_time_ms) / 1000.0)
        self._last_time_ms = now_ms

        if self.transition_timer > 0:
            self.transition_timer -= dt
            if self.transition_timer <= 0:
                self._finish_failure()
            return

        if not self.game_active:
            return

        for vehicle in self.vehicles:
            vehicle.update(road_width_px=WIDTH)

        # Goal is evaluated before timeout, so reaching the goal during this
        # frame counts as a win rather than losing a life to the timer.
        if self.frog.row == GOAL_ROW:
            self.score += 1
            self.won = True
            self.game_active = False
            return

        if check_collision(self.frog, self.vehicles, CELL_SIZE):
            self._start_failure_transition("HIT!")
            return

        self.time_remaining -= dt
        if self.time_remaining <= 0:
            self.time_remaining = 0
            self._start_failure_transition("TIME UP!")

    def draw(self, surface, font):
        from game import renderer

        renderer.draw_scene(surface, self.frog, self.vehicles)
        renderer.draw_text(surface, font, f"Lives: {self.lives}", (10, 8))
        renderer.draw_text(surface, font, f"Score: {self.score}", (160, 8))
        renderer.draw_text(
            surface,
            font,
            f"Time: {max(0, int(self.time_remaining + 0.999))}",
            (300, 8),
        )
        renderer.draw_text(
            surface,
            font,
            "Arrow keys to move. R to restart.",
            (10, HEIGHT - 24),
        )

        if self.won:
            renderer.draw_banner(surface, font, "You Won!")
        elif self.game_over:
            renderer.draw_banner(surface, font, "Game Over")
        elif self.transition_timer > 0:
            renderer.draw_banner(surface, font, self.transition_message)
