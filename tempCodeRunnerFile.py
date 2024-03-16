player_walk1_surf = pygame.image.load('./graphics/NR3.png').convert_alpha()
        player_walk1_surf = pygame.transform.rotozoom(player_walk1_surf,0,0.75)
        player_walk2_surf = pygame.image.load('./graphics/NR2.png').convert_alpha()
        player_walk2_surf = pygame.transform.rotozoom(player_walk2_surf,0,0.75)
        
        self.player_walk_list = [player_walk1_surf,player_walk2_surf]
        self.player_jump_surf = pygame.image.load('./graphics/NR4.png').convert_alpha()
        self.player_jump_surf = pygame.transform.rotozoom(self.player_jump_surf,0,0.75)